from fastapi import HTTPException


def validate_password_policy(password: str) -> None:
    digit_count = sum(char.isdigit() for char in password)
    uppercase_count = sum(char.isupper() for char in password)

    has_two_digits = digit_count >= 2
    has_two_uppercase = uppercase_count >= 2

    if not has_two_digits and not has_two_uppercase:
        raise HTTPException(
            status_code=400,
            detail="La contrasena debe tener al menos 2 numeros y al menos 2 letras mayusculas",
        )

    if not has_two_digits:
        raise HTTPException(
            status_code=400,
            detail="La contrasena debe tener al menos 2 numeros",
        )

    if not has_two_uppercase:
        raise HTTPException(
            status_code=400,
            detail="La contrasena debe tener al menos 2 letras mayusculas",
        )
