from django.shortcuts import render,redirect,get_object_or_404
from address_app.models import Address


# Create your views here.
def user_address(request):

    address = Address.objects.filter(user = request.user)
    return render(request,"user/address_app/address.html",{"address":address})

def add_address(request):
    
     
    if request.method == 'POST':
 
        name  =  request.POST.get("name")
        phone_number= request.POST.get("phone")
        alternative_phone = request.POST.get("alt_phone")
        pincode = request.POST.get("pincode")
        locality = request.POST.get("locality")
        landmark = request.POST.get("landmark")
        district = request.POST.get("district")
        state = request.POST.get("state")
        country = request.POST.get("country")
        address = request.POST.get("address")
        address_type = request.POST.get("addressType")

        Address.objects.create(
            user = request.user,
            name =name,
            phone_number = phone_number,
            alternative_phone_number =  alternative_phone,
            pincode = pincode,
            locality =  locality,
            landmark = landmark,
            district =  district,
            state = state,
            country = country,
            address = address,
            address_type = address_type
        )
        return redirect('user_address')  # Redirect to address list page after saving

    return render(request, "user/address_app/add_address.html")


def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)  
    if request.method == 'POST':
        address.name = request.POST.get("name")
        address.phone_number = request.POST.get("phone")
        address.alternative_phone_number = request.POST.get("alt_phone")
        address.pincode = request.POST.get("pincode")
        address.locality = request.POST.get("locality")
        address.landmark = request.POST.get("landmark")
        address.district = request.POST.get("district")
        address.state = request.POST.get("state")
        address.country = request.POST.get("country")
        address.address = request.POST.get("address")
        address.address_type= request.POST.get("addressType")
        address.save()
        
        return redirect('user_address')  # Redirect to address list page after saving

    return render(request,"user/address_app/edit_address.html",{'address': address})

