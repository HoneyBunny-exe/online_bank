import React, {useState} from 'react';
import {useParams} from "react-router-dom";
import "../../styles/Common.css";
import CardList from "../Home/CardList";
import './idElements.css';
import Action from "../../reUse/Action";
const CardById = () => {
    const inf= useParams()
    const [card, setCard] = useState(
        {id:1,cardType:'Дебетовая карта', cardNum:'123', balance:'11000,00'})
    return (
           <div className="page_chr">
                   <CardList/>
                <div className="infor">
                    <div className="descr">
                        <h1  className="descr_txt">МИР WorldSkills Card</h1>
                        <p className="descr_txt spec">***{card.cardNum} {card.cardType}</p>
                        <h2 className="bl">{card.balance} ₽</h2>
                    </div>
                    <div className="abil">
                        <p className="descr_txt spec">Действия</p>
                        <Action
                            path = {'/card/history/'+card.id}
                            img={'/images/history.png'}
                            height={'50'}
                            width={'50'}
                            name = {'История операций'}/>
                        <Action
                            path = {'/payment'}
                            img={'/images/pay.png'}
                            height={'50'}
                            width={'50'}
                            name = {'Оплатить'}/>
                    </div>
                    <div className="abil">
                        <Action
                            path = {'/card/rename/' + card.id}
                            img={'/images/rename.png'}
                            height={'50'}
                            width={'50'}
                            name = {'Переименовать'}/>
                        <Action
                            path = {'/card/block/' + card.id}
                            img={'/images/block.png'}
                            height={'50'}
                            width={'50'}
                            name = {'Заблокировать'}/>
                    </div>
                </div>
           </div>
    );
};

export default CardById;