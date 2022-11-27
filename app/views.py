from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .models import UserProfile, IPModel, Device, Credential, Pending
from django.views.decorators.clickjacking import xframe_options_exempt
from .forms import ProfileEditForm, CredentialForm
from django.contrib.auth.mixins import LoginRequiredMixin
import ipaddress, requests
from django.core.mail import send_mail
from cryptography.fernet import Fernet


def get_user_key(user):
    try:
        profile = UserProfile.objects.get(user=user)
        key = profile.userid.encode()
    except:
        key = False
    return key

def encrypt_data(key, data):
    try:
        f = Fernet(key)
        encrypted = f.encrypt(data.encode())
    except:
        encrypted=False
    return encrypted

def decrypt_data(key, data):
    try:
        f = Fernet(key)
        decrypted = f.decrypt(data)
        decrypted = decrypted.decode('utf-8')
    except:
        decrypted=False
    return decrypted

class Index(View):
    """
    Splashscreen or something similar
    """
    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.name == None:
                    profile.name = request.user.email.split("@")[0]
                    profile.save()
                
                if profile.email == None:
                    profile.email = request.user.email
                    profile.save()
            except:
                profile = UserProfile.objects.create(
                    user=request.user,
                    name = request.user.email.split('@')[0]
                    )
        else:
            profile = False
        
        template = 'home/index.html'
        context = {
            'profile':profile,
        }
        return render(request, template, context)

class SaveData(View, LoginRequiredMixin):
    def get(self, request, id, *args, **kwargs):
        user = request.user
        try:
            data = Pending.objects.get(endpoint=id)
        except:
            data = False
        
        if data:
            if data.owner == user:
                try:
                    profile = UserProfile.objects.get(user=user)
                except:
                    profile = False
                
                if profile:
                    key = get_user_key(user)
                    encrypted = encrypt_data(key, data.data)
                    if data.save_type.lower() == 'ip':
                        ip = IPModel(
                            owner=user,
                            ip=encrypted
                        )
                        ip.save()
                    else:
                        device = Device(
                            owner=user,
                            info=encrypted
                        )
                        device.save()
        return redirect('home')

class EmailPin(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        
        email_addr = profile.email
        send_mail(
            "PIN Reminder",
            f"Your PIN Is {profile.pin}. Please keep this pin safe. Do not store this PIN on your computer.\nRegards,\nAdmin Team",
            'admin@credentialsec.com',
            [f'{email_addr}'],
            fail_silently=True,
        )
        return redirect('home')

class ProfileView(View, LoginRequiredMixin):
    """
    Profile View Is For Logged In Users, LoginMixin Enforced View
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        ips = 0
        ip_objs = IPModel.objects.filter(owner=profile.user)
        ips = ip_objs.count

        devices = 0
        dev_obj = Device.objects.filter(owner=profile.user)
        devices = dev_obj.count

        form = ProfileEditForm(instance=profile.user)
        template = 'dash/profile.html'
        context = {
            'profile':profile,
            'form': form,
            'ips': ips,
            'devices': devices
        }
        return render(request, template, context)

class addIP(View, LoginRequiredMixin):
    """
    Class View For Adding A New IP Address To Users Profile. IP Data 
    Is Checked From The Request Meta Data And Not Input By A User.
    """
    def get(self, request, *args, **kwargs):       
        def check_ip(ip):
            # Confirm the IP is a valid IP address
            try:
                ipaddress.ip_address(ip)
                return True
            except:
                return True

        user_ip = request.META.get("REMOTE_ADDR")
        check = check_ip(user_ip)

        if check:
            user = request.user
            form = False
            next = False
            ip_list = []
            profile = UserProfile.objects.get(user=user)

            key = get_user_key(profile.user)

            try:
                ip_objects = IPModel.objects.filter(owner=profile.user)
            except:
                ip_objects = False
        
            # Find matching
            if ip_objects:
                listing = []
                for item in ip_objects:
                    enc = item.ip.encode()
                    dec = decrypt_data(key, enc)
                    listing.append(dec)
                
                for item in listing:
                    if str(user_ip) == str(item):
                        form = False
                        next = "IP Already Exists"
            else:
                next = False
                form = True

        template = 'dash/add_ip.html'
        context = {
            'user': profile,
            'form': form,
            'next': next,
            'ip': user_ip,
        }
        return render(request, template, context)
    
    def post(self, request, *args, **kwargs):
        def check_ip(ip):
            # Confirm the IP is a valid IP address
            try:
                ipaddress.ip_address(ip)
                return True
            except:
                return True

        user_ip = request.META.get("REMOTE_ADDR")
        check = check_ip(user_ip)

        if check:
            user = request.user
            form = False
            next = False
            ip_list = []
            profile = UserProfile.objects.get(user=user)

            key = get_user_key(profile.user)
            encrypted = encrypt_data(key, user_ip)

            try:
                ip_objects = IPModel.objects.filter(owner=profile.user)
            except:
                ip_objects = False
        
            # Find matching
            if ip_objects:
                listing = []
                for item in ip_objects:
                    enc = item.ip.encode()
                    dec = decrypt_data(key, enc)
                    listing.append(dec)
                
                for item in listing:
                    if str(user_ip) == str(item):
                        form = False
                        next = "IP Already Exists"
            else:
                save_info = IPModel(owner=profile.user, ip=encrypted.decode())
                save_info.save()
                next = True
                form = True

        template = 'dash/add_ip.html'
        context = {
            'user': profile,
            'form': form,
            'next': next,
            'ip': user_ip,
        }
        return render(request, template, context)

class EditProfile(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            form = ProfileEditForm(instance=profile)
        except:
            profile = False
            form = False
        template = 'dash/edit_profile.html'
        context = {
            'user': profile,
            'form':form,
            'next': False
        }
        return render(request, template, context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            form = ProfileEditForm(request.POST, instance=profile)
        except:
            profile = False
            form = False
        
        if form and form.is_valid():
            form.save()
        
        form = ProfileEditForm(instance=profile)
        template = 'dash/edit_profile.html'
        context = {
            'user': profile,
            'form':form,
            'next': True
        }
        return render(request, template, context)

class addDevice(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = False
        next = False
        device_list = []
        profile = UserProfile.objects.get(user=user)
        def device_details(self):
            family = request.user_agent.device.family
            if request.user_agent.is_mobile:
                mobile = "Yes"
            else:
                mobile = "No"
            if request.user_agent.is_tablet:
                tablet = "Yes"
            else:
                tablet = "No"
            if request.user_agent.is_pc:
                pc = "Yes"
            else:
                pc = "No"
            os = request.user_agent.os.family
            osver = request.user_agent.os.version_string
            brow = request.user_agent.browser.family
            browver = request.user_agent.browser.version_string
            out = f'Operating System: {os} {osver}\nBrowser: {brow} {browver}\nMobile: {mobile}\nTablet: {tablet}\nDesktop / Laptop: {pc}, \nFamily: {family}'
            return out

        device = device_details(self)
        
        key = get_user_key(profile.user)
        encrypted = encrypt_data(key, device)
        decoded = encrypted.decode()

        try:
            device_objects = Device.objects.filter(owner=profile.user)
        except:
            device_objects = False
        
        # Find matching
        if device_objects:
            listing = []
            for item in device_objects:
                enc = item.info.encode()
                dec = decrypt_data(key, enc)
                listing.append(dec)
            
            for item in listing:
                if str(device).lower() == str(item).lower():
                    form = False
                    next = "Device Already Exists"
        else:
            next = False
            form = True

        template = 'dash/add_device.html'
        context = {
            'user': profile,
            'form': form,
            'next': next,
            'device': device.split('\n'),
        }
        return render(request, template, context)
    
    
    def post(self, request, *args, **kwargs):
        user = request.user
        device_list = []
        profile = UserProfile.objects.get(user=user)
        def device_details(self):
            family = request.user_agent.device.family
            if request.user_agent.is_mobile:
                mobile = "Yes"
            else:
                mobile = "No"
            if request.user_agent.is_tablet:
                tablet = "Yes"
            else:
                tablet = "No"
            if request.user_agent.is_pc:
                pc = "Yes"
            else:
                pc = "No"
            os = request.user_agent.os.family
            osver = request.user_agent.os.version_string
            brow = request.user_agent.browser.family
            browver = request.user_agent.browser.version_string
            out = f'Operating System: {os} {osver}\nBrowser: {brow} {browver}\nMobile: {mobile}\nTablet: {tablet}\nDesktop / Laptop: {pc}, \nFamily: {family}'
            return out

        device = device_details(self)
        
        key = get_user_key(profile.user)
        encrypted = encrypt_data(key, device)
        decoded = encrypted.decode()


        try:
            device_objects = Device.objects.filter(owner=profile.user)
        except:
            device_objects = False
        
        # Find matching
        if device_objects:
            listing = []
            for item in device_objects:
                enc = item.info.encode()
                dec = decrypt_data(key, enc)
                listing.append(dec)
            
            for item in listing:
                if str(device).lower() == str(item).lower():
                    form = False
                    next = True
                    return redirect('profile')
        else:
            next = True
            form = True
            dev = Device(owner=profile.user, info=encrypted.decode())
            dev.save()

        template = 'dash/add_device.html'
        context = {
            'user': profile,
            'form': form,
            'next': next,
            'device': device.split('\n'),
        }
        return render(request, template, context)

class ListCredentialView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        form = CredentialForm()
        
        key = get_user_key(profile.user)
        credentials = Credential.objects.filter(owner=profile.user)
        creds = []
        for item in credentials:
            data = decrypt_data(key, item.service[2:-1].encode())
            print(data)
            creds.append({
                'service': data,
                'id': item.id
            })
        credentials = creds
        
        template = 'dash/list-credentials.html'

        context = {
            'profile': profile,
            'credentials': credentials,
            'form': form,
        }
        return render(request, template, context)


class AddCredentialView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        form = CredentialForm()
       
        template = 'dash/add_cred.html'

        context = {
            'form': form
        }
        return render(request, template, context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        form = CredentialForm(request.POST)
        key = get_user_key(profile.user)
        if form.is_valid():
            service = form.cleaned_data['service']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            service = encrypt_data(key, service)
            username = encrypt_data(key, username)
            password = encrypt_data(key, password)
            phone = encrypt_data(key, phone)
            email = encrypt_data(key, email)

            save_data = Credential(
                owner = profile.user,
                service = service,
                username = username,
                password = password,
                phone=phone,
                email=email
            )
            save_data.save()
        else:
            pass

        form = CredentialForm()        
        template = 'dash/add_cred.html'
        context = {
            'form': form,
            'next': True,
        }
        return render(request, template, context)

class ViewCredential(View, LoginRequiredMixin):
    def get(self, request, id, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        key = get_user_key(profile.user)
        known_device = False
        known_ip = False
        out = False
        strings = ""

        def check_ip(ip):
            try:
                ipaddress.ip_address(ip)
                return True
            except:
                return False

        user_ip = request.META.get("REMOTE_ADDR")
        check = check_ip(user_ip)

        if check:
            # First get the IPs and check for match
            try:
                ip_obj = IPModel.objects.filter(owner=user)
            except:
                ip_obj = False
                strings += "\nYour IP Doesn't Match Any Known IP Addresses."

            # Find matching
            if ip_obj:
                listing = []
                for item in ip_obj:
                    enc = item.ip.encode()
                    dec = decrypt_data(key, enc)
                    listing.append(dec)
                
                for item in listing:
                    if str(user_ip).lower() == str(item).lower():
                        known_ip = True

            if known_ip:
                def get_device(self):
                    family = request.user_agent.device.family
                    if request.user_agent.is_mobile:
                        mobile = "Yes"
                    else:
                        mobile = "No"
                    if request.user_agent.is_tablet:
                        tablet = "Yes"
                    else:
                        tablet = "No"
                    if request.user_agent.is_pc:
                        pc = "Yes"
                    else:
                        pc = "No"
                    os = request.user_agent.os.family
                    osver = request.user_agent.os.version_string
                    brow = request.user_agent.browser.family
                    browver = request.user_agent.browser.version_string
                    out = f'Operating System: {os} {osver}\nBrowser: {brow} {browver}\nMobile: {mobile}\nTablet: {tablet}\nDesktop / Laptop: {pc}, \nFamily: {family}'
                    return out
                
                device = get_device(self)

                try:
                    device_objects = Device.objects.filter(owner=profile.user)
                except:
                    device_objects = False
                
                # Find matching
                if device_objects:
                    listing = []
                    for item in device_objects:
                        enc = item.info.encode()
                        dec = decrypt_data(key, enc)
                        listing.append(dec)
                    
                    for item in listing:
                        if str(device).lower() == str(item).lower():
                            known_device = True
        
                
    
        if known_device and known_ip:
            try:
                cred = Credential.objects.get(owner=profile.user, id=id)
            except:
                cred=False
        
        if cred:
            key = get_user_key(user)
            service = decrypt_data(key, cred.service[2:-1].encode())
            username = decrypt_data(key,cred.username[2:-1].encode())
            password = decrypt_data(key,cred.password[2:-1].encode())
            phone = decrypt_data(key,cred.phone[2:-1].encode())
            email = decrypt_data(key,cred.email[2:-1].encode())
            stringout = False
        else:
            service = False
            username = False
            password = False
            phone = False
            stringout = "Failed To Get Details." + strings
        
        template = 'dash/cred-detail.html'

        context = {
            'service':service, 
            'username':username,
            'password':password,
            'phone':phone,
            'email':email,
            'stringout':stringout,
        }
        return render(request, template, context)