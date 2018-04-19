import React from 'react';
import {withRouter} from "react-router-dom";
import {
    Col,
    Image
} from 'react-bootstrap';

class ProfileContainer extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.content = (props.location.query) ? props.location.query.detail : null;
    }

    render() {
        const avatar_url = this.content[0].owner.avatar_url;
        // map the array of objects
        const listItems = this.content.map((repository, index) => {
            return (
                <div key={index}>
                    <p>{repository.name}</p>
                </div>
            );
        });

        return (
            <div>
                <Col xs={3} md={2}>
                    <Image src={avatar_url} thumbnail/>
                </Col>
                {listItems}
            </div>
        )
    }
}

export default withRouter(ProfileContainer);