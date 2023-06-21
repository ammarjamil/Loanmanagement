from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from Authentication.models import LoanRequest,LoanApproval,User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

import datetime

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password.'}, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials.'}, status=401)

        # Generate token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token})



class RegistrationView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if username is None or password is None:
                return Response({'error': 'Please provide both username and password.'}, status=400)
            checker=User.objects.filter(username=username)    
            if checker:
                return Response({'error': 'This User is already register.'}, status=400)
            

            user = User.objects.create_user(username=username, password=password)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token})
        except Exception as e:
            return Response({'error': e.__str__()})


class LoanrequestView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            print("in post request")
            user = request.user
            today = datetime.date.today()
         
         

            # Check if the user has a loan request in progress or open
              # Check if the user is black-listed
            if user.blacklisted:
                return Response({'message': 'You are black-listed and cannot request a loan'})
            
            if LoanRequest.objects.filter(user=user, status__in=['pending', 'approved']).exists():
                return Response({'message': 'You have a loan request in progress or open'}, status=400)

            # Check if the user has made a loan request on the same day
            if LoanRequest.objects.filter(user=user, created_date__date=datetime.date.today()).exists():
                return Response({'message': 'You have already made a loan request today'}, status=400)

            amount = int(request.data.get('amount', 0))

            # Check if the loan amount is a multiple of 500
            if amount % 500 != 0:
                return Response({'message': 'Loan amount should be a multiple of 500'}, status=400)

          # Create the loan request
            loan_request = LoanRequest.objects.create(user=user, amount=amount)

            return Response({'message': 'Loan request submitted', 'loan_request_id': loan_request.id})

        except Exception as e:
            return Response({'error': e.__str__()})

class ProcessLoanrequestView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            print(request.user.is_manager)
            loan_request_id = int(request.data.get('loan_request_id', 0))
            if loan_request_id==0:
                return Response({'message': 'loan_request_id requried'}, status=403)

            # Check if the user is a manager (additional role-based authentication may be required)
            if not request.user.is_manager:
                return Response({'message': 'You do not have permission to perform this action.'}, status=403)

            # Retrieve the loan request
            try:
                loan_request = LoanRequest.objects.get(id=loan_request_id)
            except LoanRequest.DoesNotExist:
                return Response({'message': 'Loan request not found.'}, status=404)

            # Process loan request approval or rejection
            status = request.POST.get('status')
            comment = request.POST.get('comment')

            if status == 'approved':
                loan_request.status = 'approved'
                loan_request.save()

                # Store approval details
                LoanApproval.objects.create(loan_request=loan_request, manager=request.user, status='approved', comment=comment)

                return Response({'message': 'Loan request approved successfully.'}, status=200)
            elif status == 'rejected':
                loan_request.status = 'rejected'
                loan_request.save()

                # Store rejection details
                LoanApproval.objects.create(loan_request=loan_request, manager=request.user, status='rejected', comment=comment)

                return Response({'message': 'Loan request rejected successfully.'}, status=200)
            else:
                return Response({'message': 'Invalid status provided.'}, status=400)
        except Exception as e:
            return Response({'error': e.__str__()})