import React from 'react';
import {withRouter} from "react-router-dom";
import {
    Form,
    FormGroup,
    FormControl,
    ControlLabel,
    Checkbox,
    Button,
    Col,
    Grid,
    Row
} from 'react-bootstrap';
import {fakeAuth} from "./App.js";

import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";

class LoginContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            redirectToReferrer: false,
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
    }

    handleUsernameChange(event) {
        this.setState({username: event.target.value});
    }

    handlePasswordChange(event) {
        this.setState({password: event.target.value});
    }

    handleSubmit(event) {
        axios.post('/gaz/api/v1.0/users',
            {username: this.state.username, password: this.state.password}).then(response => {
            console.log('login successfully');

            fakeAuth.authenticate(() => {
                this.setState({redirectToReferrer: true});
            });

            fakeAuth.setData(this.state.username, response.data);

            this.props.history.push("/gaz");
        }).catch(error => {
            console.log(error);
        });

        // alert('A post was submitted: ' + this.state.message);
        event.preventDefault();
    }

    render() {
        // classes must define in the parent component, and send to child components.
        return (
            <div>
                <LoginForm
                    handleSubmit={this.handleSubmit}
                    username={this.state.username}
                    password={this.state.password}
                    handleUsernameChange={this.handleUsernameChange}
                    handlePasswordChange={this.handlePasswordChange}/>
            </div>
        );
    }
}

class LoginForm extends React.Component {
    render() {
        return (
            <Grid>
                <Row className="show-grid">
                    <Form horizontal onSubmit={this.props.handleSubmit}>
                        <FormGroup controlId="formHorizontalUsername">
                            <Col componentClass={ControlLabel} sm={2} smOffset={2}>
                                GitHub Account
                            </Col>
                            <Col sm={4}>
                                <FormControl
                                    type="text"
                                    value={this.props.username}
                                    placeholder="Please use your GitHub username"
                                    onChange={this.props.handleUsernameChange}
                                    requied="true"
                                />
                            </Col>
                        </FormGroup>

                        <FormGroup controlId="formHorizontalPassword">
                            <Col componentClass={ControlLabel} sm={2} smOffset={2}>
                                Password
                            </Col>
                            <Col sm={4}>
                                <FormControl
                                    type="password"
                                    value={this.props.password}
                                    placeholder="Password"
                                    onChange={this.props.handlePasswordChange}
                                    requied="true"
                                />
                            </Col>
                        </FormGroup>

                        <FormGroup>
                            <Col smOffset={4} sm={8}>
                                <Checkbox>Remember me</Checkbox>
                            </Col>
                        </FormGroup>

                        <FormGroup>
                            <Col smOffset={4} sm={8}>
                                <Button type="submit" bsStyle="primary">Sign in</Button>
                            </Col>
                        </FormGroup>
                    </Form>
                </Row>
            </Grid>
        );
    }
}

export default withRouter(LoginContainer);