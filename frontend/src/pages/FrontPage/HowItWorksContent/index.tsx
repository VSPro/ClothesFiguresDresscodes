import React, { Fragment } from 'react';
import { useStyles } from './styles';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

interface Content {
  title: string;
  steps: Array<Step>;
  btnText: string;
}

type Step = {
  id: number;
  title: string;
};

interface Props {
  content: Content;
}

const HowItWorksContent: React.FC<Props> = ({ content }) => {
  const { title, steps, btnText } = content;
  return (
    <Fragment>
      <Typography variant="h3" color="inherit">
        {title}
      </Typography>
      <ul>
        {steps.map(step => {
          return (
            <li>
              {step.id}
              <p>{step.title}</p>
            </li>
          );
        })}
      </ul>
      <Button variant="contained">{btnText}</Button>
    </Fragment>
  );
};
export default HowItWorksContent;
