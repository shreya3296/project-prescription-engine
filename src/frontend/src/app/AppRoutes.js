import React from "react";
import { Route, Switch } from 'react-router-dom';
import Home from "../components/Home";
import Error404 from '../components/Error/404';
import Blank from "../components/Blank";
import Todo from "../components/Todo";


const AppRouter = (props) => {

  console.log("================================== AppRouter ======================================");

  return (
    <React.Fragment>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/blank" exact component={Blank} />
        <Route path="/todo" exact component={Todo} />
        <Route component={Error404} />
      </Switch>
    </React.Fragment>
  );
}

export default AppRouter;