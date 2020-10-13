from django.urls import path
from .views import (home, showLoginPage, showSignUpPage, login_view, signup_view,
        check_email_exist, check_username_exist, logout_view, showLogoutPage,
        user_profile, users, update_profile, products, add_product, delete_product,
        delete_product_view, UpdateProductView, category, add_category_view, UpdateCategoryView,
        delete_category, product_details, place_bid, bid_success, update_bid, adding_subscriber
    )


urlpatterns = [
    # Home Page | Login | Logout | Sign Up
    path("", home, name="home"),
    path("login/", showLoginPage, name="showLoginPage"),
    path("signup/", showSignUpPage, name="showSignUpPage"),
    path("login_view/", login_view, name="login_view"),
    path("logout/", showLogoutPage, name="showLogoutPage"),
    path("logout_view/", logout_view, name="logout_view"),
    path("signup_view/", signup_view, name="signup_view"),
    path("check_email_exist/", check_email_exist, name="check_email_exist"),
    path("check_username_exist/", check_username_exist, name="check_username_exist"),

    # Users Profile
    path("user/<int:id>/profile/", user_profile, name="user_profile"),
    path("users/", users, name="users"),
    path("users/<int:id>/profile/update/", update_profile, name="update_profile"),

    # Product
    path("products/", products, name="products"),
    path("product/<int:id>/details/", product_details, name="product_details"),
    path("products/add/", add_product, name="add_product"),
    path("products/<int:id>/delete", delete_product, name="delete_product"),
    path("products/<int:id>/delete/view/", delete_product_view, name="delete_product_view"),
    path("products/<int:pk>/update/", UpdateProductView.as_view(), name="update_product_view"),

    # Category
    path("category/list/", category, name="category"),
    path("category/add/", add_category_view, name="add_category_view"),
    path("category/<int:pk>/update/", UpdateCategoryView.as_view(), name="update_category_view"),
    path("category/<int:id>/delete/", delete_category, name="delete_category"),

    # Bids
    path("bids/<int:product_id>/<int:customer_id>/place/", place_bid, name="place_bid"),
    path("bids/success/", bid_success, name="bid_success"),
    path("bids/<int:customer_id>/<int:buyproduct_id>/update/", update_bid, name="update_bid"),

    # Subscribers
    path("subscribe/", adding_subscriber, name="adding_subscriber"),

]
