from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal
from .forms import GoalForm, AddAmountForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
@login_required(login_url='/authentication/login')
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)  # Don't save to database yet
            goal.owner = request.user  # Set the owner first
            goal.save()  # Now save to database
            return redirect('list_goals')

    form = GoalForm()
    return render(request, 'goals/add_goals.html', {'form': form})

@login_required(login_url='/authentication/login')
def list_goals(request):

    # goals = Goal.objects.all()
    goals = Goal.objects.filter(owner=request.user)
  
    add_amount_form = AddAmountForm() 
    return render(request, 'goals/list_goals.html', {'goals': goals, 'add_amount_form': add_amount_form})


@login_required(login_url='/authentication/login')
def add_amount(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)

    if request.method == 'POST':
        form = AddAmountForm(request.POST)
        if form.is_valid():
            additional_amount = form.cleaned_data['additional_amount']
            amount_required = goal.amount_to_save - goal.current_saved_amount

            if additional_amount > amount_required:
                messages.error(request, f'The maximum amount needed to achieve goal is : {amount_required}.')
            else:
                goal.current_saved_amount += additional_amount
                goal.save()

                # Check if the goal is achieved
                if goal.current_saved_amount == goal.amount_to_save:
                    # Send congratulatory email to the user
                        
                        send_congratulatory_email(request.user.email, goal)
                        messages.success(request, 'Congratulations! You have achieved your goal.')

                        # Disable the "Add Amount" button
                        goal.is_achieved = True
                        goal.delete()
               
                else:
                    messages.success(request, f'Amount successfully added. Total saved amount: {goal.current_saved_amount}.')
                    messages.info(request, f'Amount required to reach goal: {amount_required}.')

        return redirect('list_goals')

    # Redirect to list_goals if the request method is not POST
    return redirect('list_goals')

def send_congratulatory_email(email, goal):
    try:
        subject = 'Congratulations on achieving your goal!'
        message = f'Dear User,\n\nCongratulations on achieving your goal "{goal.name}". You have successfully saved {goal.amount_to_save}.\n\nKeep up the good work!\n\nBest regards,\nThe Goal Tracker Team, \nSmart Expense Tracker Team'
        # Email temporarily disabled to prevent authentication errors
        # send_mail(subject, message, 'hemantshirsath24@gmail.com', [email])
        print(f"Congratulatory email would be sent to {email} for goal: {goal.name}")
    except Exception as e:
        print(f"Email sending failed: {e}")
        # Continue without crashing the application
    
    



def delete_goal(request, goal_id):
    try:
        goal = Goal.objects.get(id=goal_id,owner=request.user)
        goal.delete()
        return redirect('list_goals')
    except Goal.DoesNotExist:
        pass