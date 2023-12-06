import React from 'react';
import "./Navbar.css"
import {NavLink, Routes} from "react-router-dom";

const Navbar = () => {
    return (
        <div className="navbar">
            <NavLink to='/home' >
                <img src="/images/mainIcon.png" className="navimg"/>
            </NavLink>
            <div className='left_links'>
                <NavLink to='/home' className="navbar_link">Главная</NavLink>
                <NavLink to='/pay' className="navbar_link">Платежи и переводы</NavLink>
                <NavLink to='/valute' className="navbar_link">Курсы валют</NavLink>
                <NavLink to='/bankomats' className="navbar_link">Отделения банка</NavLink>
            </div>
            <div className='right_links'>
                <NavLink to='/:login' className="navbar_link">Имя</NavLink>
            </div>
            <NavLink to='/' className="navbar_link">
                <img src="/images/exit.png" width='20' height='20' />
            </NavLink>
        </div>
    );
};
export default Navbar;