from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from calendar_app.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import logout
from django.http import JsonResponse
import datetime
from django.db.models import Q,Count
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import transaction

# Create your views here.

def adminIndex(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            counts = User.objects.aggregate(
                total_count=Count('pk')
            ) | EventManagement.objects.aggregate(
                event_count=Count('pk', filter=Q(user=request.user.id,event_status=1,is_deleted=False))
            )
            print(counts)
            return render(request, 'adminpanel/adminIndex.html',{'counts':counts})
        
        else:
            redirect('adminlogout')
    
    else:
        return redirect('adminlogin')


def adminBase(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return render(request, 'adminpanel/adminBase.html', context={})
        
        else:
            redirect('adminlogout')
    
    else:
        return redirect('adminlogin')


def adminlogin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # Optional: Check if the already logged-in user is admin/staff
            if request.user.is_superuser or request.user.is_staff:
                return redirect('adminIndex')

            else:
                return redirect('adminlogout')    
        return render(request, 'adminpanel/adminlogin.html')

    else:
        # 1. Fetch data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 2. Authenticate the user (Checks username & password against database)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # --- NEW CHECK: Allow only Superuser or Staff ---
            if user.is_superuser or user.is_staff:
                # 3. SUCCESS: User is Admin/Staff. Log them in.
                auth_login(request, user)
                return redirect('adminIndex')
            else:
                # Credentials are correct, BUT user is not authorized
                messages.error(request, "Access Denied: You do not have administrative privileges.")
                return redirect('adminlogin')
        
        else:
            # 4. FAILED: Invalid credentials (Wrong username or password)
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('adminlogin')

def adminlogout(request):
    # 1. This clears the session and user data from the request
    logout(request)
    
    # 2. Show a success message (Optional)
    messages.success(request, "You have been logged out successfully.")
    
    # 3. Redirect back to the login page
    return redirect('adminlogin')


def registeredmembers(request):
    if request.user.is_authenticated:
        # Optional: Check if the already logged-in user is admin/staff
        if request.user.is_superuser or request.user.is_staff:
            members = UserProfile.objects.filter().order_by('-id')
            print(members)
            return render(request, 'adminpanel/regsiteredmembers.html',{'members':members})
        

        else:
            return redirect('adminlogout')
    else:
        return redirect('adminlogin')


def all_events(request):
    # 1. Access Control: Superuser or Staff only
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('adminlogout')

    # 2. Setup Date/Time
    now = timezone.now()
    today_str = now.strftime('%Y-%m-%d') # For HTML min date attribute

    # 3. Filter Logic
    show_past = request.GET.get('show_past', 'false') == 'true'

    # Base Filter: Not deleted AND (Created by Superuser OR Staff)
    # We assume the 'user' field in EventManagement points to the creator
    base_query = EventManagement.objects.filter(
        Q(user__is_superuser=True) | Q(user__is_staff=True),
        is_deleted=False
    )

    if show_past:
        # Show ONLY past events (older than now)
        events = base_query.filter(event_datetime__lt=now).order_by('-event_datetime')
    else:
        # Show ONLY upcoming events (now or future)
        events = base_query.filter(event_datetime__gte=now).order_by('event_datetime')

    context = {
        'events': events,
        'now': now,
        'today_str': today_str, # Passed to restrict date picker
        'show_past': show_past
    }
    return render(request, 'adminpanel/all_events.html', context)


@require_POST
def delete_event_ajax(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})

    event_id = request.POST.get('event_id')
    
    try:
        event = EventManagement.objects.get(event_id=event_id)
        
        # Soft Delete Logic
        event.is_deleted = True
        event.event_status = 0 # Deactivate
        event.deleted_by = request.user.id
        event.deleted_reason = "Removed by Admin"
        event.save()

        return JsonResponse({'status': 'success', 'message': 'Event removed successfully!'})
    except EventManagement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Event not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@require_POST
def save_event_ajax(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})

    try:
        with transaction.atomic():
            event_id = request.POST.get('event_id')
            title = request.POST.get('event_title')
            details = request.POST.get('event_details')
            date_str = request.POST.get('event_date') # Format YYYY-MM-DD
            time_str = request.POST.get('event_time') # Format HH:MM
            circulation_type = request.POST.get('circulation_type') # 'all' or 'specific'
            selected_users = request.POST.getlist('selected_users[]') # List of User IDs

            # Combine Date and Time
            if date_str and time_str:
                dt_str = f"{date_str} {time_str}"
                event_dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                # Make it timezone aware if your settings use TZ
                event_dt = timezone.make_aware(event_dt, timezone.get_current_timezone())
                
                # Extract parts for legacy fields
                year = event_dt.year
                month = event_dt.month
                day = event_dt.day
            else:
                return JsonResponse({'status': 'error', 'message': 'Date and Time are required'})

            # Edit or Create
            if event_id:
                event = EventManagement.objects.get(event_id=event_id)
                event.last_modified_by = request.user.id
            else:
                event = EventManagement()
                event.created_by = request.user.id
                event.user = request.user

            # Set Fields
            event.event_title = title
            event.event_details = details
            event.event_datetime = event_dt
            event.event_date = day
            event.event_month = month
            event.event_year = str(year)
            event.event_status = 1
            
            # Handle Circulation Flag
            if circulation_type == 'all':
                event.circulate_to_all = True
            else:
                event.circulate_to_all = False
            
            event.save()

            # Handle EventCirculation Logic
            # 1. Clear existing circulation for this event to avoid duplicates/stale data
            EventCirculation.objects.filter(event=event).delete()

            # 2. If Specific, add new records
            if circulation_type == 'specific' and selected_users:
                circulation_entries = []
                for uid in selected_users:
                    user_obj = User.objects.get(id=uid)
                    circulation_entries.append(EventCirculation(
                        event=event,
                        user=user_obj,
                        created_by=request.user.id
                    ))
                EventCirculation.objects.bulk_create(circulation_entries)

            return JsonResponse({'status': 'success', 'message': 'Event saved successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_event_details(request):
    event_id = request.GET.get('event_id')
    try:
        event = EventManagement.objects.get(event_id=event_id)
        
        # Get Circulation Data
        circulated_users = []
        if not event.circulate_to_all:
            circ_objs = EventCirculation.objects.filter(event=event)
            for obj in circ_objs:
                circulated_users.append({'id': obj.user.id, 'name': obj.user.first_name or obj.user.username})

        data = {
            'event_id': event.event_id,
            'title': event.event_title,
            'details': event.event_details,
            'date': event.event_datetime.strftime('%Y-%m-%d'),
            'time': event.event_datetime.strftime('%H:%M'),
            'circulate_to_all': event.circulate_to_all,
            'circulated_users': circulated_users
        }
        return JsonResponse({'status': 'success', 'data': data})
    except EventManagement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Event not found'})


def search_users_ajax(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(
        Q(first_name__icontains=query) | Q(username__icontains=query)  # Assuming phone_number is in User or Profile
    ).exclude(is_superuser=True).values('id', 'first_name', 'username')[:20] # Limit results
    
    return JsonResponse({'results': list(users)})