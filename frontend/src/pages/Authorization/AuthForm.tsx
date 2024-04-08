import { useAppDispatch, useAppSelector } from "../../hooks/reduxHooks.ts"
import { useAuth } from "../../hooks/useAuth.ts"
import {
  loginByEmail,
  registerByEmail,
} from "../../store/slices/authorization/userActions.ts"
import { useInput } from "../../hooks/useInput.ts"
import { Link, Navigate, useLocation } from "react-router-dom"
import { Form } from "../../components/UI/Form/Form.tsx"
import s from "./AuthForm.module.css"
import { Input } from "../../components/UI/Input/Input.tsx"
import { Button } from "../../components/UI/Button/Button.tsx"
import { useEffect, useRef } from "react"
import { clearErrorMessage } from "../../store/slices/authorization/userSlice.ts"

interface Props {
  formType: "registration" | "authorization"
}
export const AuthForm = ({ formType }: Props) => {
  const dispatch = useAppDispatch()
  const serverError = useAppSelector((state) => state.user.errorMessage)
  const { isAuth } = useAuth()
  const location = useLocation()
  const passwordRef = useRef<HTMLInputElement | null>(null)
  const emailRef = useRef<HTMLInputElement | null>(null)
  const submitBtnRef = useRef<HTMLButtonElement | null>(null)

  useEffect(() => {
    dispatch(clearErrorMessage())
  }, [location])

  const onSubmit = (email: string, password: string) => {
    if (passwordInput.validInput && emailInput.validInput) {
      if (formType === "registration") {
        dispatch(registerByEmail({ email, password }))
      }
      if (formType === "authorization") {
        dispatch(loginByEmail({ email, password }))
      }
    } else {
      passwordRef.current?.focus()
      emailRef.current?.focus()
      submitBtnRef.current?.focus()
    }
  }
  const passwordInput = useInput("", {
    isPassword: formType === "authorization" ? undefined : true,
    isEmpty: true,
  })
  const emailInput = useInput("", {
    isEmail: true,
    isEmpty: true,
    maxLength: 100,
  })
  return isAuth === "authorized" ? (
    <Navigate to="/" />
  ) : (
    <>
      <Form
        title={
          formType === "authorization"
            ? "Главная/Войти на сайт"
            : "Главная/Регистрация"
        }
        handleSubmit={() => onSubmit(emailInput.value, passwordInput.value)}
        styles={s.form}
      >
        <Input
          type="email"
          placeholder="Email"
          {...emailInput}
          ref={emailRef}
        />
        <Input
          type="password"
          placeholder="Пароль"
          {...passwordInput}
          ref={passwordRef}
        />
        <Button type="submit" ref={submitBtnRef}>
          {formType === "authorization" ? "Войти" : "Зарегистрироваться"}
        </Button>
        {serverError && <div>{serverError}</div>}
        {formType === "authorization" && (
          <>
            <p>У вас еще нет логина?</p>
            <Link to="/registration">Зарегистрируйтесь!</Link>
          </>
        )}
      </Form>
    </>
  )
}
