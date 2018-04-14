// App.js
import React from "react";
import ReactDOM from "react-dom";
import LangsContainer from './langsContainer.js';

class App extends React.Component {
    render() {
        return (
            <div>
                <LangsContainer/>
            </div>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('react-root')
);