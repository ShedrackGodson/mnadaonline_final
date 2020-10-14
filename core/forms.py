from django import forms



class AddProductImageForm(forms.Form):
    product_photo = forms.FileField(required=True,widget=forms.FileInput(attrs={
        "class": "form-control", "id": "photo", "name": "product_photo","accept": "image/*", "type": "file"
    }))


# class Update