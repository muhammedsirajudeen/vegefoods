from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Coupon

# Create your views here.
def admin_coupon_management(request):
    coupon = Coupon.objects.all()
    
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_value = request.POST.get('discount_value')
        min_purchase_amount = request.POST.get('min_purchase_amount')  # Remove extra space
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        usage_limit = request.POST.get('usage_limit')

        if code and discount_value and min_purchase_amount and valid_from and valid_to and usage_limit:
            try:
                # Create the coupon object
                Coupon.objects.create(
                    code=code,
                    discount_value=discount_value,
                    min_purchase_amount=min_purchase_amount,
                    valid_from=valid_from,
                    valid_to=valid_to,
                    usage_limit=usage_limit
                )
                # Success message
                messages.success(request, 'Coupon created successfully!')
                return redirect('coupon_management')  # Redirect after successful creation
            except Exception as e:
                # Error message
                messages.error(request, f"Error creating coupon: {e}")
        else:
            # Error message for missing fields
            messages.error(request, "Please fill in all fields.")
    
    # Render the template with existing coupons
    return render(request, 'admin/coupon_admin.html', {'coupon': coupon})

