import React from "react";
import axios from 'axios';
import {
    Bar,
    BarChart,
    Brush,
    CartesianGrid,
    Legend,
    Line,
    LineChart,
    ReferenceLine,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts';
import {
    Col,
    Grid,
    Row,
    Panel
} from 'react-bootstrap';


axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default class ReposContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            result1: [],
            result2: []
        }
    }

    componentDidMount() {
        let self = this;
        axios.get('/gaz/api/v1.0/top_repositories').then(response => {
            console.log(response.data);
            self.setState({
                result1: response.data,
            });
        }).catch(error => {
            console.log(error);
        });

        axios.get('/gaz/api/v1.0/repository_trends').then(response => {
            console.log(response.data);
            self.setState({
                result2: response.data,
            });
        }).catch(error => {
            console.log(error);
        });
    }

    render() {
        return (
            <div>
                <ReposTrendPlots result2={this.state.result2}/>
                <TopReposPlots result1={this.state.result1}/>
            </div>
        );
    }
}

class ReposTrendPlots extends React.Component {
    render() {
        const data = this.props.result2;

        return (
            <Grid>
                <Row>
                    <Col smOffset={1} sm={10}>
                        <Panel>
                            <Panel.Heading>Repository number for each month</Panel.Heading>
                            <Panel.Body>
                                <LineChart
                                    width={900} height={600}
                                    data={data}
                                    margin={{top: 10, right: 30, left: 20, bottom: 5}}
                                >
                                    <CartesianGrid strokeDasharray="3 3"/>
                                    <XAxis dataKey="date"/>
                                    <YAxis/>
                                    <Tooltip/>
                                    <Legend/>
                                    <Line type='monotone' dataKey='total' stroke='#d62728' fill='#d62728'
                                          label={{position: 'top'}}/>
                                    <Brush/>
                                </LineChart>
                            </Panel.Body>
                        </Panel>
                    </Col>
                </Row>
            </Grid>
        );
    }
}

class TopReposPlots extends React.Component {
    render() {
        const data = this.props.result1;

        return (
            <Grid>
                <Row>
                    <Col smOffset={1} sm={10}>
                        <Panel>
                            <Panel.Heading>The most popular 100 repositories</Panel.Heading>
                            <Panel.Body>
                                <BarChart
                                    width={900} height={600}
                                    data={data}
                                    margin={{top: 5, right: 30, left: 20, bottom: 5}}
                                >
                                    <CartesianGrid strokeDasharray="3 3"/>
                                    <XAxis dataKey="name"/>
                                    <YAxis/>
                                    <Tooltip/>
                                    <Legend verticalAlign="top" wrapperStyle={{lineHeight: '40px'}}/>
                                    <ReferenceLine y={0} stroke='#000'/>
                                    <Brush dataKey='name' height={30} stroke="#8884d8"/>
                                    <Bar dataKey="star_num" fill="#ffc658"/>
                                </BarChart>
                            </Panel.Body>
                        </Panel>
                    </Col>
                </Row>
            </Grid>
        );
    }
}