from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from . models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import logout
from django.http import JsonResponse
import datetime
from django.db.models import Q

# Create your views here.


# First Page - App Install Prompt
def index(request):
    return render(request, 'index.html')

# Second Page - Calendar with Slider
def calendar_view(request):
    return render(request, 'calendar.html')

def demo(request):
    return render(request,'calendar1.html')


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # Redirect directly to 'login' (This creates a clean URL)
            return redirect('demo')
        return render(request, 'loginSignup.html')

    else:
        # 1. Fetch data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 2. Authenticate the user (Checks username & password against database)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 3. SUCCESS: Create the session and log them in
            auth_login(request, user)
            
            # Optional: Add a welcome message if you want
            # messages.success(request, "Login Successful")
            
            # Redirect to the 'demo' URL as requested
            return redirect('demo') 
        
        else:
            # 4. FAILED: Invalid credentials
            messages.error(request, "Invalid username or password. Please try again.")
            
            # Redirect back to the login page to show the error
            return redirect('login')



def signup(request):
    if request.method == 'POST':
        try:
            # 1. Fetch Data from the HTML Form
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # 2. Basic Validation: Check passwords match
            # if password != confirm_password:
            #     messages.error(request, "Password and Confirm Password do not match.")
            #     return redirect('signup')

            # 3. Check if Username is already taken
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken. Please choose another one.")
                return redirect('signup')

            # 4. Check if Mobile Number is already registered 
            if UserProfile.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "This mobile number is already registered.")
                return redirect('signup')

            # 5. Create the User in Django Auth System
            user = User.objects.create_user(username=username, password=password)
            user.first_name = full_name  # Saving full name in first_name field
            user.save()

            # 6. Save Phone Number (Create the Profile/Member object)
            profile = UserProfile(user=user, phone_number=phone_number)
            profile.save()

            # 7. Success Message and Redirect
            messages.success(request, "Registration successful! Please login with your credentials.")
            return redirect('login')

        except IntegrityError:
            # Captures database errors (like duplicate unique fields)
            messages.error(request, "An account with these details already exists.")
            return redirect('signup')
            
        except Exception as e:
            # Captures any other unexpected errors and prints to console for debugging
            print(f"Signup Error: {e}")
            messages.error(request, "Something went wrong during registration. Please try again.")
            return redirect('signup')
    
    else:
        # GET request: just render the page
        if request.user.is_authenticated:
           return redirect('demo')
        
        return render(request, 'loginSignup.html')


def logout_view(request):
    # 1. This clears the session and user data from the request
    logout(request)
    
    # 2. Show a success message (Optional)
    messages.success(request, "You have been logged out successfully.")
    
    # 3. Redirect back to the login page
    return redirect('login')



def get_events_for_date(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get parameters from GET request
    day = request.GET.get('day')
    month = request.GET.get('month')
    year = request.GET.get('year')
    print("136",request.GET)

    try:
        # Query your EventManagement model
        events = EventManagement.objects.filter(
            user=request.user,
            event_date=int(day),
            event_month=int(month),
            event_year=str(year),
            is_deleted=False, # Ensure we don't fetch deleted events
            event_status=1    # Ensure we fetch active events
        ).values('event_title', 'event_details', 'event_id')

        # Convert QuerySet to list
        events_list = list(events)
        print(events_list)
        
        return JsonResponse({'status': 'success', 'events': events_list})
    except Exception as e:
        print(f"Error fetching events: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})


def add_event_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            # 1. Get Data from Form
            day = request.POST.get('day')
            month = request.POST.get('month')
            year = request.POST.get('year')
            title = request.POST.get('event_title')
            details = request.POST.get('event_details')
            time_str = request.POST.get('event_time') # "14:30" or empty

            # 2. Construct DateTime object
            # (If user didn't pick time, default to 00:00)
            if time_str:
                hour, minute = map(int, time_str.split(':'))
            else:
                hour, minute = 0, 0

            # Create standard python datetime object
            event_dt = datetime.datetime(int(year), int(month), int(day), hour, minute)

            # 3. Save to Database
            new_event = EventManagement(
                user=request.user,
                event_title=title,
                event_details=details,
                event_date=int(day),
                event_month=int(month),
                event_year=str(year),
                event_datetime=event_dt,
                event_status=1, # Active
                created_by=request.user.id
            )
            new_event.save()

            messages.success(request, "Event added successfully!")
            return redirect('demo') # Redirect back to calendar

        except Exception as e:
            print(f"Error saving event: {e}")
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('demo')

    else:
        # --- GET REQUEST (Show the Form) ---
        day = request.GET.get('day')
        month = request.GET.get('month')
        year = request.GET.get('year')

        # Convert numeric month to Name (e.g., 1 -> January)
        month_name = datetime.date(2025, int(month), 1).strftime('%B')

        context = {
            'day': day,
            'month': month,
            'month_name': month_name,
            'year': year
        }
        return render(request, 'add_event.html', context)
    

def update_event_view(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')
    # 1. Fetch the event securely (ensure it belongs to the logged-in user)
    event = get_object_or_404(EventManagement, event_id=event_id, user=request.user)

    if request.method == 'POST':
        try:
            # 2. Update Data
            event.event_title = request.POST.get('event_title')
            event.event_details = request.POST.get('event_details')
            
            # Handle Time Update
            time_str = request.POST.get('event_time')
            if time_str:
                hour, minute = map(int, time_str.split(':'))
                # Create new datetime object keeping the original date
                event.event_datetime = event.event_datetime.replace(hour=hour, minute=minute)
            
            event.last_modified_by = request.user.id
            event.save()

            messages.success(request, "Event updated successfully!")
            return redirect('demo')

        except Exception as e:
            print(f"Error updating: {e}")
            messages.error(request, "Failed to update event.")
            return redirect('demo')

    else:
        # 3. GET Request - Show Form Pre-filled
        
        # Extract time for the HTML input (HH:MM format)
        existing_time = ""
        if event.event_datetime:
            existing_time = event.event_datetime.strftime('%H:%M')
            
        # Get Month Name for display
        month_name = datetime.date(2025, event.event_month, 1).strftime('%B')

        context = {
            'is_update': True,  # Flag to change UI text
            'event': event,     # Pass object to template
            'day': event.event_date,
            'month': event.event_month,
            'month_name': month_name,
            'year': event.event_year,
            'existing_time': existing_time
        }
        return render(request, 'update_event.html', context)
    

def remove_event_view(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Fetch event to ensure ownership
    event = get_object_or_404(EventManagement, event_id=event_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Soft delete logic
            event.is_deleted = True
            event.event_status = 0
            event.save()
            
            messages.success(request, "Event removed successfully!")
            return redirect('demo') # Redirect to calendar view
        except Exception as e:
            print(f"Error removing: {e}")
            messages.error(request, "Failed to remove event.")
            return redirect('update_event', event_id=event_id)
            
    return redirect('demo')



def my_events_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # 1. Base Query: Active events for logged-in user
    # Fixed: Used 'event_status=1' as per your model (1=Active)
    events_query = EventManagement.objects.filter(
        user=request.user, 
        is_deleted=False,
        event_status=1 
    )

    # 2. Get Filter Parameters
    search_query = request.GET.get('q', '')
    filter_date = request.GET.get('filter_date', '')
    filter_month = request.GET.get('filter_month', '')

    # 3. Apply Filters
    if search_query:
        # Search by title or details
        events_query = events_query.filter(
            Q(event_title__icontains=search_query) | 
            Q(event_details__icontains=search_query)
        )
    
    if filter_date:
        # Filter by specific full date (YYYY-MM-DD)
        # Django automatically handles the string to date comparison here
        events_query = events_query.filter(event_datetime__date=filter_date)
    
    elif filter_month:
        # Filter by specific month (YYYY-MM)
        try:
            y, m = filter_month.split('-')
            events_query = events_query.filter(event_year=y, event_month=m)
        except ValueError:
            pass # Prevent error if date format is wrong
        
    else:
        # DEFAULT: If no specific filter, show Current & Future events
        # Fixed: Using datetime.datetime.now() because of 'import datetime'
        events_query = events_query.filter(event_datetime__gte=datetime.datetime.now())

    # 4. Order by Date (Crucial for grouping)
    events = events_query.order_by('event_datetime')

    # 5. Grouping Logic (Month -> Events)
    grouped_events = []
    current_group_key = None
    current_group_dict = None

    for event in events:
        # Ensure we have a datetime object
        if event.event_datetime:
            dt = event.event_datetime
            group_key = dt.strftime('%B %Y') # e.g., "November 2025"
            
            if group_key != current_group_key:
                # Save previous group if it exists
                if current_group_dict:
                    grouped_events.append(current_group_dict)
                
                # Start new group
                current_group_key = group_key
                current_group_dict = {
                    'month_name': group_key,
                    'month_idx': dt.month,
                    'year': dt.year,
                    'default_day': 1, # Default day for the 'Add Event' button
                    'events': []
                }
            
            # Add event to the current group
            current_group_dict['events'].append(event)
    
    # Append the last group after the loop finishes
    if current_group_dict:
        grouped_events.append(current_group_dict)

    context = {
        'grouped_events': grouped_events,
        'search_query': search_query,
        'filter_date': filter_date,
        'filter_month': filter_month
    }
    return render(request, 'my_events_list.html', context)
