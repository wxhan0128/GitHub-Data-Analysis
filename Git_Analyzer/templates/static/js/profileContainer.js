import React from 'react';
import {withRouter} from "react-router-dom";
import {
    Grid,
    Row,
    Col,
    Image,
    ListGroup,
    ListGroupItem,
    Panel
} from 'react-bootstrap';
import {
    PieChart,
    Pie,
    Legend,
    Tooltip
} from 'recharts';
import Enumerable from 'linq';

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
                    <Col xs={12} sm={4}>
                        <Panel>
                            <Panel.Body>
                                <Profile userData={this.userData}/>
                                <hr/>
                                <ReposPlots content={this.content}/>
                            </Panel.Body>
                        </Panel>

                    </Col>
                    <Col xs={12} sm={8}>
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

class ReposPlots extends React.Component {
    render() {
        const dataArray = this.props.content;
        // use linq.js to do advance process on json data, e.g. group by, count or sum
        // the pie chart component only identify name-value pair
        const query = Enumerable.from(dataArray)
            .groupBy("$.language", null, "{ name: $, value: $$.count() }")
            .toArray();

        return (
            <div>
                <h5>Language distribution</h5>
                <PieChart width={330} height={400}>
                    <Pie data={query} cx="50%" cy="30%" innerRadius={40} outerRadius={80} fill="#82ca9d" label/>
                    <Tooltip/>
                </PieChart>
            </div>
        );
    }
}

// must use withRouter, otherwise it will unable to find props.location variable
export default withRouter(ProfileContainer);