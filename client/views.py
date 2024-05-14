from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import artiste,Annonce,Comment,product,panier,Message
from django.contrib.auth.models import User
from .serializer import standard_serializer,Artiste_Serializer,login_serializer,annonce_home_serializer,product_home_serializer,user_info_serializer,All_Message_Serializer
from django.contrib.auth import login,authenticate
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
import uuid

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        # Initialize serializer with request data
        user_serializer = login_serializer(data=request.data)
        
        # Validate serializer data
        if user_serializer.is_valid():
            # Extract username and password from validated data
            username = request.data.get('username')
            password = request.data.get('password')
            
            # Authenticate user
            user =User.objects.get(username=username)
            if user is not None:
                # If user is authenticated, log in the user
                login(request, user)
                return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)
            else:
                # If authentication failed, return appropriate response
                return Response({"message": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # If serializer data is invalid, return 400 Bad Request
            return Response( status=status.HTTP_400_BAD_REQUEST)
    else:
        # If request method is not POST, return 405 Method Not Allowed
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



     

@api_view(['POST'])
def standard_signup(request):
    if request.method == 'POST':
        user_serializer = standard_serializer(data=request.data)

        if user_serializer.is_valid():
            # Save user without password
            user = user_serializer.save()

            # Set password for the user
            password = request.data.get('password')
            user.set_password(password)
            
            # Save user again to update the password
            user.save()

            return Response({"message": "Standard user sign-up successful"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def artiste_signup(request):
    if request.method == 'POST':
        artiste_serializer = Artiste_Serializer(data=request.data)  # Instantiate the serializer

        if artiste_serializer.is_valid():
            # Access validated data
            validated_data = artiste_serializer.validated_data

            # Extract user-related data
            user_data = validated_data.get('user', {})  # Get user data from validated_data

            # Create user without saving to database yet
            user = User.objects.create_user(username=user_data.get('username'), email=user_data.get('email'))

            # Set password for the user
            user.set_password(user_data.get('password'))

            # Save user
            user.save()

            # Create artiste instance and set additional fields
            artiste_instance = artiste.objects.create(user=user, preuve=validated_data.get('preuve'), profession=validated_data.get('profession'))

            return Response({"message": "Artiste sign-up successful"}, status=status.HTTP_201_CREATED)

        return Response({"error": artiste_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET','POST'])
def home(request):
  if request.method=='GET':
    # Fetch all annonces
    annonces = Annonce.objects.all()
    # Serialize annonces with their number of comments
    annonces_data = []
    for annonce in annonces:
        comment_count = annonce.comments.count()
        serialized_annonce = annonce_home_serializer(annonce).data
        serialized_annonce['comment_count'] = comment_count
        annonces_data.append(serialized_annonce)

    # Fetch all products
    products = product.objects.all()
    # Serialize products
    products_data = product_home_serializer(products, many=True).data

    # Fetch user info
    user_info = request.user
    # Serialize user info
    user_info_serialized = user_info_serializer(user_info).data

    # Prepare the response data
    response_data = {
        'annonces': annonces_data,
        'products': products_data,
        'user': user_info_serialized
    }
    
    # Return the response
    return Response(response_data)
  if request.method=='POST':
      product_id=request.data.get('product_id')
      try:
         product_reference=product.objects.get(id=product_id)
      except product.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
      panier_item,created=panier.object.get_or_create(owner=request.user,product=product_reference)
      if not created:
          panier_item.quantity+=1
          panier_item.save()
   


@api_view(['GET'])
def all_conversations(request):
    if request.method == 'GET':
        user_id = request.user.id
        message_data = []
        users = User.objects.exclude(id=user_id)  # Exclude the current user
        for user in users:
            user2_id = user.id
            last_message = Message.objects.filter(
                Q(sender=user2_id, receiver=user_id) | Q(sender=user_id, receiver=user2_id)
            ).order_by('-date', '-time').first()
            if last_message:
                # Format the time in the desired format
                last_message_time = last_message.time.strftime('%H:%M:%S')
                # Serialize the message data
                last_message_data = All_Message_Serializer(last_message).data
                # Add formatted time to the serialized data
                last_message_data['formatted_time'] = last_message_time
                message_data.append(last_message_data)
        response = {
            'data': message_data
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'PUT'])
def conversation(request):
    if request.method == 'GET':
        user1_id = request.GET.get('user1_id')
        user2_id = request.GET.get('user2_id')
        
        # Update last message is_seen status
        last_message = Message.objects.filter(
            Q(sender=user1_id, receiver=user2_id) | Q(sender=user2_id, receiver=user1_id)
        ).order_by('-date', '-time').first()
        if last_message:
            last_message.is_seen = True
            last_message.save()

        # Fetch all messages between user1 and user2
        all_messages = Message.objects.filter(
            Q(sender=user1_id, receiver=user2_id) | Q(sender=user2_id, receiver=user1_id)
        ).order_by('-date', '-time')
        
        # Serialize messages
        all_messages_serialized = All_Message_Serializer(all_messages, many=True)
        return Response(all_messages_serialized.data)
    
    elif request.method == 'PUT':
        content = request.data.get('message')
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Receiver with the provided ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # Save last message is_seen status
        last_message = Message.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        ).order_by('-date', '-time').first()
        if last_message:
            last_message.is_seen = True
            last_message.save()
        
        # Create new message
        message = Message.objects.create(content=content, sender=sender, receiver=receiver)
        return Response({"message": "Message sent successfully."}, status=status.HTTP_201_CREATED)
    


@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        user_email = request.data.get('email')
        if user_email:
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=404)

            # Generate unique token for password reset
            confirmation_code = random.randint(1000, 9999)

            # Store confirmation code in session
            request.session['confirmation_code'] = confirmation_code

            # Send email with confirmation code
            subject = '7arfa Password Reset'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = '7arfa2024@gmail.com'  # Sender's email address
            recipient_list = [user_email]  # List of recipient email addresses

            send_mail(subject, message, from_email, recipient_list)

            return Response({"message": "Email sent successfully."})
        else:
            code_confirmation_test = request.data.get("code")
            if code_confirmation_test:
                # Retrieve confirmation code from session
                session_confirmation_code = request.session.get('confirmation_code')
                if code_confirmation_test == session_confirmation_code:
                    # Clear confirmation code from session after successful verification
                    request.session.pop('confirmation_code', None)
                    return Response({"message": "Code is valid."})
                else:
                    return Response({"message": "Wrong code."}, status=400)
            else:
                new_password = request.data.get("new_password")
                if new_password:
                    try:
                      user = User.objects.get(email=request.data.get("email_new"))
                        
                  

                      user.set_password(new_password)
                      user.save()
                      return Response({"message":"password change succefly"})
                         
                    
                    except User.DoesNotExist:
                        return Response({"message": "User not found."}, status=404)
                else:
                    return Response({"message": "Please provide a new password."}, status=400)