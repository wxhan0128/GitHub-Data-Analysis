// App.js
import React from "react";
import ReactDOM from "react-dom";
import {
    BrowserRouter as Router,
    Route,
    Switch,
    withRouter
} from "react-router-dom";
import {
    LinkContainer
} from 'react-router-bootstrap';
import {
    Navbar,
    Nav,
    NavItem,
    NavDropdown,
    MenuItem,
    Grid,
    Row,
    Col,
    FormGroup,
    FormControl,
    Button
} from 'react-bootstrap';
import LangsContainer from './langsContainer.js';
import LoginContainer from './loginContainer.js';
import ProfileContainer from './profileContainer.js';

class Home extends React.Component {
    render() {
        return (
            <div>
                <Grid>
                    <Row className="show-grid">
                        <Col sm={6} md={8}>
                            <LangsContainer/>
                        </Col>
                    </Row>
                </Grid>
            </div>
        );
    }
}

class About extends React.Component {
    render() {
        return (
            <div>
                About!
            </div>
        );
    }
}

class Login extends React.Component {
    render() {
        return (
            <div>
                <LoginContainer/>
            </div>
        );
    }
}

class Management extends React.Component {
    render() {
        return (
            <div>
                <ProfileContainer/>
            </div>
        );
    }
}

export const fakeAuth = {
    isAuthenticated: false,
    username: null,
    userPackage: null,
    authenticate(cb) {
        this.isAuthenticated = true;
        setTimeout(cb, 100); // fake async
    },
    setData(name, data) {
        this.username = name;
        this.userPackage = data;
    },
    signout(cb) {
        this.isAuthenticated = false;
        this.username = null;
        this.userPackage = null;
        setTimeout(cb, 100);
    }
};

const AuthButton = withRouter(
    ({history}) =>
        fakeAuth.isAuthenticated ? (
            <NavDropdown eventKey={3} title="Welcome!" id="basic-nav-dropdown">
                <MenuItem eventKey={3.1} onClick={() =>
                    history.push({
                            pathname: `/gaz/user/${fakeAuth.username}`,
                            query: {
                                detail: fakeAuth.userPackage
                            },
                        }
                    )}>
                    {fakeAuth.username}
                </MenuItem>
                <MenuItem divider/>
                <MenuItem eventKey={3.2} onClick={() => {
                    fakeAuth.signout(() => history.push("/gaz"));
                }}>Sign Out</MenuItem>
            </NavDropdown>
        ) : (
            <LinkContainer to="/gaz/login">
                <NavItem eventKey={2}>
                    Login
                </NavItem>
            </LinkContainer>
        )
);

class NavBar extends React.Component {
    constructor() {
        super();
        this.state = {
            isLogedIn: 'False',
        };
    }

    render() {
        return (
            <Navbar>
                <Navbar.Header>
                    <LinkContainer to="/gaz">
                        <Navbar.Brand>
                            GitHub Analyzer
                        </Navbar.Brand>
                    </LinkContainer>
                </Navbar.Header>
                <Nav>
                    <LinkContainer to="/gaz/about">
                        <NavItem eventKey={1}>
                            About
                        </NavItem>
                    </LinkContainer>
                    <AuthButton/>
                </Nav>
            </Navbar>
        );
    }
}

class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <NavBar/>

                    <Switch>
                        <Route exact path="/gaz" component={Home}/>
                        <Route path="/gaz/about" component={About}/>
                        <Route path="/gaz/login" component={Login}/>
                        <Route path="/gaz/user/:name" component={Management}/>
                    </Switch>
                </div>
            </Router>
        );
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('react-root')
);