import pandas as pd
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from quiz.models import Question, Subject, Topic
from user.models import CustomUser
from chat.models import Message
from .decorators import admin_only
from .forms import QuestionForm, CustomUserForm, AdminProfileForm, ExcelUploadForm

admin_models = [
			{'app_label': 'quiz', 'model_name':'subject'},
			{'app_label': 'quiz', 'model_name':'topic'},
		]

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('custom_admin:home')
        else:
            messages.error(request, 'Invalid credentials or not authorized')

    return render(request, 'admin/custom_login.html')

@admin_only
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('custom_admin:admin_login')

@method_decorator(admin_only, name='dispatch')
class HomeView(View):
	"""Admin home view."""
	def get(self, request, *args, **kwargs):
		return render(request, 'admin/home.html', {'admin_models':admin_models})

@method_decorator(admin_only, name='dispatch')
class QuestionListView(View):
    """List and filter questions."""
    def get(self, request, *args, **kwargs):
        subject_filter = request.GET.get('subject')
        topic_filter = request.GET.get('topic')
        search_query = request.GET.get('search')

        subjects = Subject.objects.all()
        topics = Topic.objects.filter(subject__id=subject_filter) if subject_filter else Topic.objects.all()

        questions_list = Question.objects.all()
        if subject_filter:
            questions_list = questions_list.filter(topic__subject__id=subject_filter)
        if topic_filter:
            questions_list = questions_list.filter(topic__id=topic_filter)
        if search_query and search_query.strip():
            questions_list = questions_list.filter(Q(text__icontains=search_query))

        questions_list = questions_list.order_by('-id')
        paginator = Paginator(questions_list, 10)  # 10 questions per page
        page_number = request.GET.get('page')
        questions = paginator.get_page(page_number)

        return render(request, 'admin/question/list.html', {
            'questions': questions,
            'subjects': subjects,
            'topics': topics,
            'subject_filter': subject_filter,
            'topic_filter': topic_filter,
            'search_query': search_query,
        })

@method_decorator(admin_only, name='dispatch')
class QuestionEditView(View):
    """Edit an existing question."""
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = QuestionForm(instance=question)
        return render(request, 'admin/question/edit.html', {'form': form, 'question': question})

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully.')
            return redirect('custom_admin:update', question_id=question.id)

        return render(request, 'admin/question/edit.html', {'form': form, 'question': question})

@method_decorator(admin_only, name='dispatch')
class QuestionAddView(View):
    """Add a new question."""
    def get(self, request):
        form = QuestionForm()
        return render(request, 'admin/question/add.html', {'form': form})

    def post(self, request):
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save()
            messages.success(request, 'Question added successfully.')
            return redirect('custom_admin:update', question_id=question.id)

        return render(request, 'admin/question/add.html', {'form': form})

@admin_only
def upload_questions_from_excel(request):
    """Upload questions from an Excel file"""
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            
            # Validate if the uploaded file is an Excel file
            if not (excel_file.name.endswith('.xlsx') or excel_file.name.endswith('.xls')):
                messages.error(request, 'Please upload a valid Excel file with .xlsx or .xls extension.')
                return redirect('custom_admin:upload_questions')
            
            try:
                # Read the Excel file
                df = pd.read_excel(excel_file)
                
                # Define the required columns for the Question model
                required_columns = [
                    'text', 'subject', 'topic', 'correct_answer', 
                    'option_a', 'option_b', 'option_c', 'start_time', 
                    'end_time', 'is_repeatable'
                ]
                
                # Check if all required columns are present
                if not all(col in df.columns for col in required_columns):
                    messages.error(request, 'Excel file must contain the following columns: text, subject, topic, correct_answer, option_a, option_b, option_c, start_time, end_time, is_repeatable.')
                    return redirect('custom_admin:upload_questions')
                
                # Process each row in the Excel file
                for _, row in df.iterrows():
                    # Explicitly find or create the Subject
                    subject = Subject.objects.filter(name=row['subject']).first()
                    if subject is None:
                        subject = Subject.objects.create(name=row['subject'])

                    # Explicitly find or create the Topic
                    topic = Topic.objects.filter(name=row['topic'], subject=subject).first()
                    if topic is None:
                        topic = Topic.objects.create(name=row['topic'], subject=subject)

                    # Parse start and end times, if provided
                    start_time = pd.to_datetime(row['start_time'], errors='coerce')
                    end_time = pd.to_datetime(row['end_time'], errors='coerce')
                    
                    # Handle potential non-datetime entries
                    if pd.isnull(start_time):
                        start_time = None
                    if pd.isnull(end_time):
                        end_time = None

                    # Convert is_repeatable to boolean
                    is_repeatable = bool(row['is_repeatable'])

                    # Create a new question entry
                    Question.objects.create(
                        text=row['text'],
                        correct_answer=row['correct_answer'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        start_time=start_time,
                        end_time=end_time,
                        is_repeatable=is_repeatable,
                        topic=topic
                    )

                messages.success(request, 'Questions have been successfully uploaded!')
                return redirect('custom_admin:questions')
                
            except Exception as e:
                messages.error(request, f'An error occurred while processing the file: {e}')
                return redirect('custom_admin:upload_questions')
    
    else:
        form = ExcelUploadForm()

    return render(request, 'admin/question/upload_excel.html', {'form': form})



@method_decorator(admin_only, name='dispatch')
class QuestionDeleteView(View):
    """Delete a question."""
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        return redirect('custom_admin:questions')


@method_decorator(admin_only, name='dispatch')
class CustomUserListView(View):
    """List all users."""
    def get(self, request):
        users = CustomUser.objects.all()

        # Filter by is_active if specified
        is_active_filter = request.GET.get('is_active')
        if is_active_filter:
            users = users.filter(is_active=is_active_filter.lower() == 'true')

        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            users = users.filter(Q(email__icontains=search_query) | Q(first_name__icontains=search_query))

        return render(request, 'admin/user/list.html', {'users': users, 'search_query': search_query, 'is_active_filter': is_active_filter})

@method_decorator(admin_only, name='dispatch')
class CustomUserEditView(View):
    """Edit an existing user."""
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = CustomUserForm(instance=user)
        return render(request, 'admin/user/edit.html', {'form': form, 'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = CustomUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('custom_admin:user_update', user_id=user.id)

        return render(request, 'admin/user/edit.html', {'form': form, 'user': user})

@method_decorator(admin_only, name='dispatch')
class CustomUserAddView(View):
    """Add a new user."""
    def get(self, request):
        form = CustomUserForm()
        return render(request, 'admin/user/add.html', {'form': form})

    def post(self, request):
        form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, 'User added successfully.')
            return redirect('custom_admin:user_update', user_id=user.id)

        return render(request, 'admin/user/add.html', {'form': form})

@method_decorator(admin_only, name='dispatch')
class CustomUserDeleteView(View):
    """Delete a user."""
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('custom_admin:users')


@admin_only
def update_admin_profile(request):
    """
    View to update the admin's profile information.
    """
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('custom_admin:admin_update')
    else:
        form = AdminProfileForm(instance=request.user)

    return render(request, 'admin/profile/edit.html', {'form': form})


@admin_only
def chat_user_messages_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(user=user)
    messages.filter(seen_by_admin=False).update(seen_by_admin=True)
    return render(request, 'admin/chat/user_messages.html', {'messages': messages, 'user': user})

@admin_only
def chat_user_list_view(request):
    # Yangi xabarlari bo'lgan foydalanuvchilar
    new_users = Message.objects.filter(seen_by_admin=False).values('user_id').distinct()
    new_user_ids = [user['user_id'] for user in new_users]
    unique_new_users = CustomUser.objects.filter(id__in=new_user_ids)

    # Har bir foydalanuvchi uchun yangi xabarlar sonini hisoblash
    new_users_with_counts = []
    for user in unique_new_users:
        count = user.message_set.filter(seen_by_admin=False).count()
        new_users_with_counts.append({'user': user, 'new_message_count': count})

    # Arxivdagi foydalanuvchilar (barcha xabarlar uchun)
    archived_users = CustomUser.objects.exclude(id__in=new_user_ids)

    return render(request, 'admin/chat/user_list.html', {
        'new_users': new_users_with_counts,
        'archived_users': archived_users
    })