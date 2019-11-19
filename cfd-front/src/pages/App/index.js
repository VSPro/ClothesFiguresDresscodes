
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'
// import logo from './logo.svg';
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
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <span>Обхват груди</span>
        <input type='number' value={ inputs.first } onChange={ inputValidationFunc('first') } />
        <span>Обхват талии</span>
        <input type='number' value={ inputs.second } onChange={ inputValidationFunc('second') } />
        <span>Обхват бёдер</span>
        <input type='number' value={ inputs.third } onChange={ inputValidationFunc('third') } />
        <span>Рост</span>
        <input type='number' value={ inputs.fourth } onChange={ inputValidationFunc('fourth') } />
        <button
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
        </button>

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
