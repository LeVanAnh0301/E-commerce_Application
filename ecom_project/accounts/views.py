from re import split
from carts.models import Cart, CartItem
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from .forms import RegistrationForm
from accounts.models import Account
from carts.views import cart_id


# đăng kí 
def register(request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name, last_name = last_name,email=email, phone_number = phone_number, username= username)
            user.phone_number = phone_number
            user.save()

            current_site= get_current_site(request=request) # lấy site hiện tại để xác định domain cho các demain sau 
            mail_subject ='Activate your blog account'
            # tạo tiêu đề với nội dung email 
            message = render_to_string("accounts/activate_email.html",{
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)

            })
            # gửi email 
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            message.success(
                request=request, 
                message = ' Please confirm youremail address to complete the rgistration'
            )
            return redirect('register')
        else: 
            message.error(request=request,message='Register failed')
    else: 
        form = RegistrationForm()
        context = {
            'form': form,
        }
    return render(request,'accounts/register.html',context)


         # Thông báo và chuyển hướng

'''
# Chú thích về cách hoạt động của function logic 
1. Khi request được yêu cầu qua method "POST": hệ thống sẽ check username, password. Việc xác thực sẽ được thực hiện thông qua biến user ( method xác thực auth.authenticate)
Nếu user chính xác ( is not None), ta thực hiện chỉnh sửa hoạt động của giỏ hàng khi xác thực người dùng 




'''
# đăng nhập 
def login(request):
    if request.method == 'POST': 
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)
        if user is not None:  # Đoạn code dưới lập trình việc hiển thị giỏ hàng sau khi xác thực người dùng
            try: 
                cart = Cart.objects.get(cart_id=cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart) # Lấy tất cả các mục trong giỏ hàng (cart items) liên quan đến giỏ hàng đã lấy ở bước trước.
                if cart_items.exists():
                    product_variation = []
                    for cart_item in cart_items: 
                        variations = cart_items.variations.all()
                        product_variation.append(list(variations))
                    
                    cart_items = CartItem.objects.filter(user=user)
                    existing_variation_list = [list(item.variations.all() for item in cart_items)] # tạo ra list các item tồn tại trong db liên quan với cart_item
                    id = [item.id for item in cart_items]

                    for product in product_variation: # sẽ ứng dụng vào thực tế nào ? 
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user 
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart) # phân biệt trường hợp if và else:? 
                            for item in cart_items: 
                                item.user = user 
                                item.save()
            except Exception: 
                pass 
            auth.login(request= request, user=user)
            messages.success(request=request,message='Login successful!')

            url = request.META.get('HTTP_REFERER')
            try: 
                query = request.utils.urlparse(url).query 
                params = dict(x.split("=") for x in query.split('&'))
                if "next" in params:
                    next_page = params['next']
                    return redirect(next_page)
                pass
            except Exception:
                return redirect('dashboard')
        else:
            # xem lại đoạn code này ???
            messages.error(request=request, message="Login failed!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request,'accounts/login.html',context=context)
'''
Đoạn mã trên thực hiện việc phân tích một URL để trích xuất các tham số từ chuỗi truy vấn (query string). 

query = request.utils.urlparse(url).query: Dòng này sử dụng hàm urlparse từ module utils trong package request. Nó nhận một URL làm đối số và trả về một đối tượng ParseResult chứa thông tin phân tích của URL. query được gán bằng phần chuỗi truy vấn (query string) của URL.

params = dict(x.split("=") for x in query.split('&')): Dòng này tiếp tục phân tích chuỗi truy vấn để tạo ra một từ điển (dictionary) 
chứa các tham số từ chuỗi truy vấn. 
Đầu tiên, query.split('&') tách chuỗi truy vấn thành các cặp tham số, 
với mỗi cặp được phân tách bằng dấu "&". Sau đó, vòng lặp for x in query.split('&') lặp qua các cặp tham số. 
Trong mỗi lần lặp, x.split("=") tách cặp tham số thành key và value, với dấu "=" làm dấu phân cách.
Cuối cùng, dict(...) tạo ra từ điển bằng cách sử dụng các key và value tách rời.

Ví dụ:

Giả sử có một URL như sau: https://example.com/search?keyword=python&category=programming&sort=desc

Sử dụng đoạn mã trên:

url = "https://example.com/search?keyword=python&category=programming&sort=desc"
Sau khi thực thi dòng query = request.utils.urlparse(url).query, giá trị của query sẽ là "keyword=python&category=programming&sort=desc".
Tiếp theo, dòng params = dict(x.split("=") for x in query.split('&')) sẽ phân tích query thành từ điển params với các cặp key-value tương ứng với các tham số trong chuỗi truy vấn:
params = {   "keyword": "python",   "category": "programming",   "sort": "desc" }

'''

                    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request=request, message=' You are logout')
    return redirect('login')


def activate(request,uidb64, token):
    # xem lại code 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Your account is activated, please login!")
        return render(request, 'accounts/login.html')
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect('home')

@login_required(login_url='login')
def dashboard(request): 
    return render(request,'accounts/dashboard.html')


def forgot_password(request): # lập trình cho chức năng quên mật khẩu
    try: 
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Account.objects.get(email_exact=email)

        current_site = get_current_site(request=request)
        mail_subject = 'Reset your password'
        message = render_to_string('accounts/reset_password_email.html',{
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
       })
        send_email = EmailMessage(mail_subject, message, to=[email])
        send_email.send()

        messages.success(request=request, message="Password reset email has been sent to your email address")
    except Exception: 
        messages.error(request=request, message="Account does not exists")
    finally: 
        context = {
    'email': email if 'email' in locals() else '',

        }
        return render(request,'accounts/forgotPassword.html',context=context)


def reset_password_validate(request,uidb64, token):
    try: 
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None 

    if user is not None and default_token_generator(user,token):
        request.session['uid'] = uid 
        messages.info(request=request, message = 'Please reset your password')
        return redirect('reset_password')
    else: 
        messages.error(request=request, message = 'This link has been required')
        return redirect('home')




def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password: 
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.seccess(request, message = "Password reset successfil!")
            return redirect('login') # ?
        else: 
            messages.error(request,message='Password doesn/t match. Please enter the passsword')
    return render(request,'accounts/reset_password.html')

        








