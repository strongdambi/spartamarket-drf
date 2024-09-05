from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email 
from .models import User

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



def validate_profile_update(current_user, target_username, new_email):
    # 사용자 권한 검증
    if current_user.username != target_username:
        raise ValidationError("권한이 없어 프로필을 수정할 수 없습니다.")

    # 이메일 중복 검증
    if new_email and new_email != current_user.email and User.objects.filter(email=new_email).exists():
        raise ValidationError("이미 사용 중인 이메일입니다.")

