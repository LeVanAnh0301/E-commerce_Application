from django import forms 
from django.forms import CharField, widgets 
from .models import Account



class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password'
    }))
    confirmed_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password'
    }))

    class Meta: 
        model = Account 
        fields =['first_name','last_name','phone_number','email','password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['place_holder'] = ' Enter last_name'
        self.fields['phone_number'].widget.attrs['place_holder'] = 'Enter phone_number'
        self.fields['email'].widget.attrs['place_holder'] = 'Enter email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirmed_password')

        if  password != confirmed_password:
            raise forms.ValidationError(
                'Password does not match!'
            )
'''Đoạn mã trên đúng là một ModelForm của Django được sử dụng để tạo ra một form đăng ký (RegistrationForm) dựa trên model Account. Dưới đây là giải thích chi tiết:

Khởi tạo Form:

class RegistrationForm(forms.ModelForm): khai báo một class là RegistrationForm kế thừa từ forms.ModelForm.
Dinh dạng các trường của Form:

Mỗi trường của form được định nghĩa như là một thuộc tính của class RegistrationForm. Ví dụ: first_name, last_name, phone_number, email, password, confirmed_password.
Class Meta:

class Meta là một lớp trong ModelForm giúp định nghĩa metadata của form. Trong trường hợp này, model = Account chỉ định model được sử dụng là Account và fields =['first_name','last_name','phone_number','email','password'] chỉ định các trường dữ liệu từ model sẽ được sử dụng trong form.
init Method:

__init__ method được sử dụng để tùy chỉnh hoặc thêm các thuộc tính của form khi nó được khởi tạo. Trong trường hợp này, nó được sử dụng để thêm thuộc tính placeholder và class cho các trường của form.
Method clean:

clean method được sử dụng để kiểm tra và làm sạch dữ liệu sau khi người dùng gửi form. Trong trường hợp này, nó kiểm tra xem password và confirmed_password có khớp nhau không. Nếu không khớp, nó sẽ raise một ValidationError với thông báo 'Password does not match!'.
Tóm lại, đoạn mã này định nghĩa một form đăng ký với các trường nhất định và thực hiện kiểm tra sự khớp nhau của mật khẩu và mật khẩu xác nhận.
'''     
  