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
    ControlLabel,
    Form,
    FormControl,
    FormGroup,
    Grid,
    Row,
    Button
} from 'react-bootstrap';


axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default class LangsContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            result1: [],
            result2: [],
            lname: '',
        };

        this.handleLanguageSubmit = this.handleLanguageSubmit.bind(this);
        this.handleLanguageChange = this.handleLanguageChange.bind(this);
    }

    componentDidMount() {
        let self = this;
        axios.get('/gaz/api/v1.0/languages').then(response => {
            console.log(response.data);
            self.setState({
                result1: response.data,
            });
        }).catch(error => {
            console.log(error);
        });
    }

    handleLanguageChange(event) {
        this.setState({lname: event.target.value});
    }

    handleLanguageSubmit(event) {
        let self = this;
        axios.post('/gaz/api/v1.0/language_trends',
            {lname: this.state.lname}).then(response => {
            console.log('submit successfully');

            self.setState({
                result2: response.data
            });
        }).catch(error => {
            console.log(error);
        });

        event.preventDefault();
    }

    render() {
        return (
            <div>
                <LangsPlots result1={this.state.result1}/>
                <TrendPlots
                    result2={this.state.result2}
                    handleLanguageSubmit={this.handleLanguageSubmit}
                    handleLanguageChange={this.handleLanguageChange}
                />
            </div>
        );
    }
}

class LangsPlots extends React.Component {
    render() {
        const data = this.props.result1;

        return (
            <Grid>
                <Row>
                    <Col smOffset={1} sm={10}>
                        <BarChart
                            width={900} height={600}
                            data={data}
                            margin={{top: 5, right: 30, left: 20, bottom: 5}}
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

class TrendPlots extends React.Component {
    render() {
        const data = this.props.result2;

        return (
            <Grid>
                <Row>
                    <Col smOffset={1} sm={10}>
                        <Form inline onSubmit={this.props.handleLanguageSubmit}>
                            <FormGroup controlId="formControlsSelect">
                                <ControlLabel>Select</ControlLabel>{'  '}
                                <FormControl componentClass="select" placeholder="select"
                                             onChange={this.props.handleLanguageChange}>
                                    <option value="JavaScript">JavaScript</option>
                                    <option value="Python">Python</option>
                                    <option value="Java">Java</option>
                                    <option value="C">C</option>
                                    <option value="C++">C++</option>
                                    <option value="Swift">Swift</option>
                                </FormControl>
                            </FormGroup>{'  '}
                            <FormGroup>
                                <Button type="submit" bsStyle="primary">Confirm</Button>
                            </FormGroup>
                        </Form>
                    </Col>
                </Row>

                <Row>
                    <Col smOffset={1} sm={10}>
                        <LineChart
                            width={900} height={600}
                            data={data}
                            syncId="anyId"
                            margin={{top: 10, right: 30, left: 0, bottom: 0}}>
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="date"/>
                            <YAxis/>
                            <Tooltip/>
                            <Line type='monotone' dataKey='total' stroke='#82ca9d' fill='#82ca9d'/>
                            <Brush/>
                        </LineChart>
                    </Col>
                </Row>
            </Grid>
        );
    }
}