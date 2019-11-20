
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'
// import logo from './logo.svg';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import './App.css';

// import TestContainer from '../TestContainer/'

function App( props ) {
  
  const [inputs, setInputs] = useState({
    first: '',
    second: '',
    third: '',
    fourth: ''
  })
  const typeOfShape = useSelector( state => state.app.typeOfShape)

  const inputValidationFunc = (field) => {
    return ( e ) => { 
      const value = e.target.value 
      // Здесь можно добавить проверок, но всё это надо выносить в отдельный компонент
      if(value < 350) {
        setInputs(
          (state) => {
            return {...state, [field]: value}
          }
        )
      }
    }
  }

  const dispatch = useDispatch()

  return (
    <div className="App">
      <header className="App-header">
        <TextField
          id="chest-girth"
          label="Обхват груди"
          variant="outlined"
          // fullWidth
          margin="normal"
          type='number'
          value={ inputs.first }
          onChange={ inputValidationFunc('first') }
        />
        <TextField
          id="waist-circumference"
          label="Обхват талии"
          variant="outlined"
          margin="normal"
          type='number'
          value={ inputs.second }
          onChange={ inputValidationFunc('second') }
        />
        <TextField
          id="hip-girth"
          label="Обхват бёдер"
          variant="outlined"
          margin="normal"
          type='number'
          value={ inputs.third }
          onChange={ inputValidationFunc('third') }
        />
        <TextField
          id="height"
          label="Рост"
          variant="outlined"
          margin="normal"
          type='number'
          value={ inputs.fourth }
          onChange={ inputValidationFunc('fourth') }
        />
        <Button
          variant="contained"
          color="secondary"
          disabled={ !(inputs.first && inputs.second && inputs.third && inputs.fourth) } 
          onClick={ () => { 
            dispatch(
              {
                type: 'SHAPE_METRICS', 
                payload: {
                  chest: inputs.first,
                  waist: inputs.second,
                  hips: inputs.third,
                  height: inputs.fourth
                } 
              }
            ) 
          }}
        >
          Определить тип фигуры  
        </Button>

        <div>
          <div>Ваш тип фигуры:</div>
          { typeOfShape }
        </div>

        {/* <TestContainer /> */}
      </header>
    </div>
  );
}

export default App;
