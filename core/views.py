from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from core.models import (BuyProduct, Category, 
            Product, UserProfile, Subscriber
    )
from core.forms import AddProductImageForm
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


User = get_user_model()

def home(request):
    """ This is home page """

    return render(request, "core/index.html", {
        "products": Product.objects.all()
    })


def showLoginPage(request):
    """ This is to show the login page """
    return render(request, "core/login.html", {

    })
    

def showSignUpPage(request):
    """ This is to the sign up page """
    return render(request, "core/signup.html", {

    })


@csrf_exempt
def login_view(request):
    """ This is for user to login """
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(
        username = username,
        password = password
    )
    if user is not None:
        login(request, user)
        messages.success(request, "Logged In Successfully.", fail_silently=False)
        return redirect("home")
    else:
        messages.error(request, "Invalid Login Credentials.", fail_silently=False)
        return redirect("showLoginPage")


@login_required(login_url="showLoginPage")
def showLogoutPage(request):
    """ This is shows the logout form """
    return render(request, "core/logout.html", {})


@csrf_exempt
def logout_view(request):
    """ This is for user to logout """
    logout(request) # Logout request user
    messages.info(request, "You have logged out successfully.", fail_silently=False)
    return redirect("showLoginPage")


@csrf_exempt
def signup_view(request):
    """ This is for user to sign up """
    username = request.POST.get("username")
    password = request.POST.get("password")
    c_password = request.POST.get("c_password")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    address = request.POST.get("address")

    try:
        if password == c_password: # Checking if the two passwords match
            obj = User.objects.create_user(
                username = username,
                email = email,
                phone = phone,
                address = address
                )
            obj.set_password(c_password)
            obj.save()
            login(request, obj) # Login User After Account Been Created.
            messages.success(request, "Your account is successfully created.", fail_silently=False)
            return redirect("home")
        else:
            messages.error(request, "Passwords did'nt match.", fail_silently=False)
            return redirect("showSignUpPage")
    except:
        messages.error(request, "Failed to create an account. Username and/or Email seems to already exists.", fail_silently=False)
        return redirect("showSignUpPage")


@csrf_exempt
def check_email_exist(request):
    """ This is to check if the email entered on the form is already existing """
    email = request.POST.get("email")
    user_obj = User.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    """ This is to check if the username entered on the form is already existing """
    username = request.POST.get("username")
    user_obj = User.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required(login_url="showLoginPage")
def user_profile(request, id):
    """ This is to view the user profile """

    return render(request, "core/profile.html",{
        "user": User.objects.get(id=id)
    })


@login_required(login_url="showLoginPage")
@permission_required("view_users","add_users","change_users")
def users(request):
    """ This is to view the list system users: Only admins can see the list """

    return render(request, "core/users.html", {
        "users": User.objects.filter(
            is_superuser=False
        )
    })


@csrf_exempt
def update_profile(request, id):
    """ This is to update the user profile """
    username = request.POST.get("username")
    first_name, last_name = request.POST.get("fullname").split()
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    address = request.POST.get("address")

    userObj = User.objects.get(id=id)
    userObj.first_name = first_name
    userObj.last_name= last_name
    userObj.username= username
    userObj.email = email
    userObj.phone = phone
    userObj.address = address
    userObj.save()
    messages.success(request, "Your profile is successfully update.", fail_silently=False)
    return redirect("user_profile", id)
    

@login_required(login_url="showLoginPage")
@permission_required("view_product","add_product")
def products(request):
    """ This is to view the list of priducts """

    return render(request, "core/products.html", {
        "products": Product.objects.all()
    })


@login_required(login_url="showLoginPage")
@permission_required("view_product","add_product")
def add_product(request):
    """ This is to add a new product """
    if request.method == "POST":
        name = request.POST.get("product_name")
        price = request.POST.get("product_price")
        category = request.POST.get("product_category")
        photo = request.POST.get("product_photo")
        description = request.POST.get("product_description")
        new = request.POST.get("new")
        used = request.POST.get("used")
        valid_until = request.POST.get("valid_until")
        
        form = AddProductImageForm(request.POST, request.FILES or None)
        if form.is_valid():
            image = form.cleaned_data.get("product_photo")

        product_object = Product.objects.create(
            name = name,
            price = price,
            description = description,
            category = Category.objects.get(id=int(category)),
            image = image,
            valid_until = valid_until
        )
        if new is not None:
            product_object.new = True
        if used is not None:
            product_object.new = False
        product_object.save()
        messages.success(request, "Product successfully added.", fail_silently=False)
        return redirect("products")

    return render(request, "core/add_product.html",{
        "category_list": Category.objects.all(),
        "form": AddProductImageForm()
    })


@login_required(login_url="showLoginPage")
@permission_required("view_product","delete_product")
def delete_product(request, id):
    """ This is to view product delete form """

    return render(request, "core/delete_product.html", {
        "object": Product.objects.get(id=id)
    })


@csrf_exempt
def delete_product_view(request, id):
    """ This is to delete the product """
    Product.objects.get(id=id).delete()
    messages.success(request, "Product deleted successfully.")
    return redirect("products")


class UpdateProductView(LoginRequiredMixin, UpdateView):
    """ This is for updating a product """
    model = Product
    fields = ["name", "price", "image", "description", "category", "new", "valid_until"]
    exclude = (
        "sold",
    )
    template_name = "core/update_product.html"
    success_message = "Product Successfully Updated."
    success_url = "/products"
    

@login_required(login_url="showLoginPage")
@permission_required("view_category","delete_category")
def category(request):
    """ This is to view the list of categories """

    return render(request, "core/category_list.html", {
        "category_list": Category.objects.all()
    })


@login_required(login_url="showLoginPage")
@permission_required("add_category","change_category")
def add_category_view(request):
    """ This is for showing add category page and handling requests for adding new category """
    if request.method == "POST":
        name = request.POST.get("category_name")
        try:
            Category.objects.create(
                name = name
            )
            messages.success(request, "Category added successfully.", fail_silently=False)
            return redirect("category")
        except:
            messages.error(request, "Failed to add category. Name provided seems to already exists.")
            return redirect("add_category_view")

    return render(request, "core/add_category.html", {
        
    })


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    """ This is for updating a category """
    model = Category
    fields = "__all__"
    template_name = "core/update_category.html"
    success_message = "Category Successfully Updated."
    success_url = "/category/list/"


@login_required(login_url="showLoginPage")
@permission_required("view_category","delete_category")
def delete_category(request, id):
    """ This is to view category delete form and handling delete category request """

    if request.method == "POST":
        Category.objects.get(id=id).delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("category")

    return render(request, "core/delete_category.html", {
        "object": Category.objects.get(id=id)
    })


@login_required(login_url="showLoginPage")
def product_details(request, id):
    object = Product.objects.get(id=id)

    bought_products = BuyProduct.objects.filter(
        product=object
    )
    bought_products_customers = list()
    for _ in bought_products:
        bought_products_customers.append(_.customer.username)

    return render(request, "core/product_detail.html", {
        "object": object,
        "bought_products": bought_products,
        "bought_products_customers": bought_products_customers,
        "now": timezone.now()
    })


@login_required(login_url="showLoginPage")
def place_bid(request, product_id, customer_id):
    productObj = Product.objects.get(id=product_id)
    customerObj = UserProfile.objects.get(id=customer_id)

    if request.method == "POST":
        bid_price = request.POST.get("bid_price")
        BuyProduct.objects.create(
            customer_price = bid_price,
            product = productObj,
            customer = customerObj
        )
        messages.success(request, "Bid Placed Successfully.", fail_silently=False)
        return redirect("bid_success")

    return render(request, "core/place_bid.html", {
        "product": productObj
    })


@login_required(login_url="showLoginPage")
def update_bid(request, customer_id, buyproduct_id):
    product = Product.objects.get(id=buyproduct_id)
    customerObj = UserProfile.objects.get(id=customer_id)

    bpObj = BuyProduct.objects.filter(
        product = product,
        customer = customerObj
    ).first()

    if request.method == "POST":
        bpObj.customer_price = request.POST.get("bid_price")
        bpObj.save()
        messages.success(request, "Bid Updated Successfully.", fail_silently=False)
        return redirect("product_details", product.id)

    return render(request, "core/update_bid.html", {
        "bpObj": bpObj
    })


@login_required(login_url="showLoginPage")
def bid_success(request):
    return render(request, "core/bid_success.html")


@csrf_exempt
def adding_subscriber(request):
    Subscriber.objects.create(
        email = request.POST.get("email")
    )
    