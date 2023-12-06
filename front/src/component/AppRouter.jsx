import React from 'react';
import {Route, Routes, useNavigate} from "react-router-dom";
import {privateRoutes} from "./router";
import Home from "./pages/Home/Home";
import App from "../App";

const AppRouter = () => {
    const router = useNavigate()
    return (
       <Routes>
           {privateRoutes.map(route=>
           <Route
               path={route.path}
               element={route.component}
               key = {route.path}/>
           )}
           <Route element={Home}/>
       </Routes>
    );
};

export default AppRouter;