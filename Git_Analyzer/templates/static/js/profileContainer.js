import React from 'react';
import {withRouter} from "react-router-dom";
import {
    Grid,
    Row,
    Col,
    Image,
    ListGroup,
    ListGroupItem
} from 'react-bootstrap';

class ProfileContainer extends React.Component {
    constructor(props, context) {
        super(props, context);

        this.content = (props.location.query) ? props.location.query.detail : null;
        this.userData = this.content[0].owner;
    }

    render() {
        return (
            <Grid>
                <Row>
                    <Col smOffset={2} xs={12} sm={2}>
                        <Profile userData={this.userData}/>
                    </Col>
                    <Col xs={12} sm={6}>
                        <ListGroup>
                            <ReposList content={this.content}/>
                        </ListGroup>
                    </Col>
                </Row>
            </Grid>
        )
    }
}

class Profile extends React.Component {
    render() {
        return (
            <div>
                <Image width={120} height={120} src={this.props.userData.avatar_url} thumbnail/>
                <p>{this.props.userData.login}</p>
            </div>
        );
    }

}

class ReposList extends React.Component {
    render() {
        // map the array of objects
        const listItems = this.props.content.map((repository, index) => {
            return (
                <ListGroupItem key={index}>
                    <h5>
                        <a href={repository.html_url}>{repository.name}</a>
                    </h5>
                    <p>Build date: {repository.created_at}</p>
                    <p>Main language: {repository.language}</p>
                    <p>Total stars: {repository.stargazers_count}</p>
                </ListGroupItem>
            );
        });

        return (
            <div>
                {listItems}
            </div>
        )
    }
}

export default withRouter(ProfileContainer);