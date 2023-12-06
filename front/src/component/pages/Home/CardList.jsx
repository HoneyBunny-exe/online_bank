import React, {useState} from 'react';
import './CardList.css'
import CardItem from "./CardItem";
import CreditCard from "./CreditCard";
import BillItem from "./BillItem";
const CardList = () => {
    const [cards, setCards] = useState([
        {id:1,cardType:'Дебетовая карта', cardNum:'123', balance:'11000,00'},
        {id:2,cardType:'Кредитная карта', cardNum:'253', balance:'1500,12'},
        {id:3,cardType:'Дебетовая карта', cardNum:'188', balance:'250000,65'}
    ])
    const [bills, setBills] = useState([
        {billType:'Текущий счет', billNum:'458', balance:'25000,45'},
        {billType:'Текущий счет', billNum:'485', balance:'280,05'}
    ])
    const [credits, setCredits] =useState([
        {creditType:'Кредит наличными', creditNum:'789',balance:'90999,45', datePay:'19.12.23'},
        {creditType:'Ипотека', creditNum:'658',balance:'1250000,48', datePay:'12.01.24'}
    ])
    return (
        <div className="card_list">
            <p className="tit">Мои Карты</p>
            <div className="cardl">
                {cards.map((card)=>
                    <CardItem card={card}/>
                )}
            </div>
            <p className="tit">Мои Счета</p>
            <div className="cardl">
                {bills.map((bill)=>
                    <BillItem bill={bill}/>
                )}
            </div>
            <p className="tit">Мои Кредиты</p>
            <div className="cardl">
                {credits.map((credit)=>
                <CreditCard credit={credit}/>
                )}
            </div>
        </div>
    );
};

export default CardList;