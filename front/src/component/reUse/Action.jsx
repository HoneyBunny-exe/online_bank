import React from 'react';
import './Action.css'
import {useNavigate} from "react-router-dom";
const Action = (props) => {
    const router = useNavigate()
    return (
        <div onClick={()=> router(props.path)}
            className="action">
            <img className="act_img" src={props.img}/>
            <p className='act_txt'>{props.name}</p>
        </div>
    );
};

export default Action;