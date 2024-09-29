from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . models import Coupon
from django.http import JsonResponse


def admin_coupon_management(request):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('admin_login') 
    coupon = Coupon.objects.all()
    
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_value = request.POST.get('discount_value')
        min_purchase_amount = request.POST.get('min_purchase_amount')  
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        usage_limit = request.POST.get('usage_limit')

        if code and discount_value and min_purchase_amount and valid_from and valid_to and usage_limit:
            try:
             
                Coupon.objects.create(
                    code=code,
                    discount_value=discount_value,
                    min_purchase_amount=min_purchase_amount,
                    valid_from=valid_from,
                    valid_to=valid_to,
                    usage_limit=usage_limit
                )
               
                messages.success(request, 'Coupon created successfully!')
                return redirect('coupon_management')  
            except Exception as e:
                
                messages.error(request, f"Error creating coupon: {e}")
        else:
          
            messages.error(request, "Please fill in all fields.")
    

    return render(request, 'admin/coupon_admin.html', {'coupon': coupon})


def delete_coupon(request,coupon_id):
    
    coupen = get_object_or_404(Coupon,id=coupon_id)
    coupen.delete()
    messages.success(request, 'Coupon deleted successfully!')
    return redirect('coupon_management')


def edit_coupon(request,coupon_id):

    coupon = get_object_or_404(Coupon,id = coupon_id)

    if request.method == 'POST':
        coupon.code = request.POST.get('code')
        coupon.discount_value = request.POST.get('discount_value')  
        coupon.min_purchase_amount = request.POST.get('min_purchase_amount')  
        coupon.valid_from = request.POST.get('valid_from')
        coupon.valid_to = request.POST.get('valid_to')
        coupon.usage_limit = request.POST.get('usage_limit')


        coupon.save()
        
        messages.success(request,"success update")
        return redirect('coupon_management')

    return render(request, 'admin/edit_coupon.html', {'coupon': coupon})
