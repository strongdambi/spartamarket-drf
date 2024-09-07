from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email 
from django.contrib.auth.hashers import check_password
from .models import User

# 회원가입 검증
def validate_user_data(signup_data):
    # 사용자 입력 데이터를 검증 후 필드별로 오류 메시지를 딕셔너리 형태로 반환
    err_msg_dict = {}

    # 데이터 추출
    username = signup_data.get('username')
    email = signup_data.get('email')
    password = signup_data.get('password')
    password_check = signup_data.get('password_check')

    # 사용자명 유일성 검증
    if User.objects.filter(username=username).exists():
        err_msg_dict['username'] = "이미 존재하는 사용자명입니다."

    # 비밀번호 일치 여부 검증
    if password != password_check:
        err_msg_dict['password'] = "비밀번호가 일치하지 않습니다."

    # 이메일 형식 검증 및 중복 여부 확인
    try:
        django_validate_email(email)  # 이메일 형식 검증
    except ValidationError:
        err_msg_dict['email'] = "올바른 이메일 형식이 아닙니다."
    
    if User.objects.filter(email=email).exists():
        err_msg_dict['email'] = "이미 사용 중인 이메일입니다."

    # 오류 메시지 딕셔너리가 비어 있으면 유효성 통과
    if not err_msg_dict:
        return True, None

    # 오류가 있으면 False와 오류 메시지 딕셔너리 반환
    return False, err_msg_dict


# 프로필 업데이트 검증
def validate_profile_update(current_user, target_username, new_email):
    # 오류 메시지 딕셔너리 초기화
    err_msg_dict = {}

    # 사용자 권한 검증
    if current_user.username != target_username:
        err_msg_dict['permission'] = "권한이 없어 프로필을 수정할 수 없습니다."

    # 이메일 중복 검증
    if new_email and new_email != current_user.email and User.objects.filter(email=new_email).exists():
        err_msg_dict['email'] = "이미 사용 중인 이메일입니다."

    # 오류 메시지 딕셔너리가 비어 있으면 유효성 통과
    if not err_msg_dict:
        return True, None

    # 오류가 있으면 False와 오류 메시지 딕셔너리 반환
    return False, err_msg_dict



# 리프레시 토큰 검증
def validate_refresh_token(refresh_token_str):
    if not refresh_token_str:
        raise ValidationError({"refresh_token": "refresh_token is required."})

    try:
        # 리프레시 토큰 객체 생성 및 유효성 검사
        return RefreshToken(refresh_token_str)
    except TokenError:
        raise ValidationError({"refresh_token": "This token is already blacklisted."})


# 비밀번호 변경 검증
def validate_password_change(user, current_password, new_password, new_password_confirm):
    err_msg_dict = {}

    # 현재 비밀번호가 일치하는지 확인
    if not check_password(current_password, user.password):
        err_msg_dict['current_password'] = "현재 비밀번호가 일치하지 않습니다."

    # 새 비밀번호와 확인 비밀번호가 일치하는지 확인
    if new_password != new_password_confirm:
        err_msg_dict['new_password'] = "새 비밀번호가 일치하지 않습니다."

    # 새 비밀번호가 기존 비밀번호와 동일한지 확인
    if check_password(new_password, user.password):
        err_msg_dict['new_password_same'] = "새 비밀번호가 기존 비밀번호와 같을 수 없습니다."

    if err_msg_dict:
        raise ValidationError(err_msg_dict)


# 계정 삭제 시 비밀번호 검증
def validate_delete_account(user, password):
    if not check_password(password, user.password):
        raise ValidationError({"password": "비밀번호가 일치하지 않습니다."})