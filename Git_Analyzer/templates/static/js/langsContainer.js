import React from "react";
import axios from 'axios';
import {
    BarChart,
    Bar,
    Brush,
    ReferenceLine,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
} from 'recharts';
import {
    Col,
    Grid,
    Row
} from 'react-bootstrap';


axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default class LangsContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
            message: '',
        };
    }

    componentDidMount() {
        let self = this;
        axios.get('/gaz/api/v1.0/languages').then(response => {
            console.log(response.data);
            self.setState({
                results: response.data,
                message: 'load all language data!',
            });
        }).catch(error => {
            console.log(error);
        });
    }

    render() {
        return (
            <div>
                <LangsPlots results={this.state.results}/>
            </div>
        );
    }
}

class LangsPlots extends React.Component {
    render() {
        const data = this.props.results;

        return (
            <Grid>
                <Row>
                    <Col smOffset={1} sm={10}>
                        <BarChart
                            width={900} height={600}
                            data={data}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="language"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend verticalAlign="top" wrapperStyle={{lineHeight: '40px'}}/>
                            <ReferenceLine y={0} stroke='#000'/>
                            <Brush dataKey='language' height={30} stroke="#8884d8"/>
                            <Bar dataKey="total" fill="#8884d8"/>
                        </BarChart>
                    </Col>
                </Row>
            </Grid>
        );
    }
}