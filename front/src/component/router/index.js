import Home from "../pages/Home/Home";
import ValuteCourse from "../pages/ValuteCourse";
import Bankomats from "../pages/Bankomats";
import LK from "../pages/LK";
import CardById from "../pages/GetItemById/CardById";
import Payment from "../pages/CardAbility/Transfer";
import CardHistory from "../pages/CardAbility/history/CardHistory";
import Transfer from "../pages/CardAbility/Transfer";
import TopUp from "../pages/CardAbility/TopUp";
import Block from "../pages/CardAbility/Block";
export const privateRoutes=[
    {path:"/home", component:<Home/>},
    {path:'/pay', component: <Payment/>},
    {path:':login', component: <LK/>},
    {path:'/valute', component: <ValuteCourse/>},
    {path:'/bankomats', component: <Bankomats/>},
    {path:'/cards/:id', component: <CardById/>},
    {path:'/card/history/:id', component: <CardHistory/>},
    {path:'/card/transfer/:id', component: <Transfer/>},
    {path:'/card/plus/:id', component: <TopUp/>},
    {path:'/card/block/:id', component: <Block/>}
]