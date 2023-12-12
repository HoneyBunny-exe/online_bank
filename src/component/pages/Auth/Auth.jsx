import React, {useContext, useState} from 'react';
import '../../styles/Common.css'
import './Auth.css'
import {set} from "react-hook-form";
import {useNavigate} from "react-router-dom";
import {ATMS} from "../../utils/consts";
import {AuthContext} from "../../../context";
const Auth = () => {
    const{isAuth, setIsAuth} = useContext(AuthContext)
    const router = useNavigate()
    const[state, setState] = useState('SignIn')
    const siqnIn=()=>{
        //запрос
       setIsAuth(true)
    }
    const inital=()=>{
        setState('Reg')
    }
    const finalReg=()=>{
        //запрос
        setState('regSuc')
    }
    return (
        <div className="page_chr">
            {state ==='SignIn' &&
            <div className="reg__modal">
                <h1 className='head__reg'>Добро пожаловать!</h1>
                <input className='reg__input'
                placeholder='Логин'
                />
                <input className='reg__input'
                placeholder='Пароль'
                />
                <button onClick={siqnIn}
                    className="reg__button">Продолжить</button>
                <div className='reg__nav'>
                    <button  onClick={()=>setState('SignUp')} className='reg__link'>Зарегистрироваться</button>
                    <button onClick={()=>router(ATMS)} className='reg__link'>Ближайшие банкоматы</button>
                </div>
            </div>
            }
            {state ==='SignUp' &&
                <div className='reg__modal'>
                    <button onClick={()=>setState('SignIn')}
                        className='reg__link'>На главную</button>
                    <h1 className='head__reg'>Регистрация</h1>
                    <p>Введите номер счета</p>
                    <input className='reg__input'
                        />
                    <button onClick={inital}
                        className="reg__button">Продолжить</button>
                </div>
            }
            {
                state==='Reg' &&
                <div className="reg__modal">
                    <button onClick={()=>setState('SignIn')}
                            className='reg__link'>На главную</button>
                    <h3>Логин</h3>
                    <input className="reg__input"/>
                    <h3>Пароль</h3>
                    <input className="reg__input"/>
                    <button onClick={finalReg}
                        className="reg__button">Зарегистрироваться</button>
                </div>
            }
            {state==='regSuc'&&
                <div className="reg__modal">
                    <div style={{marginTop:"auto", marginBottom:"auto"}}>
                        <h1 className='head__reg'>Регистрация прошла успешно!</h1>
                        <button
                            onClick={()=>setState('SignIn')}
                            className="reg__button"
                            style={{marginLeft:"8%"}}>
                            Войти</button>
                    </div>
                </div>
            }
        </div>
    );
};

export default Auth;