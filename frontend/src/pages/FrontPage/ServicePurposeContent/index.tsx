import React, { Fragment } from 'react';
import { useStyles } from './styles';
import Typography from '@material-ui/core/Typography';

interface Content {
  title: string;
  description: string;
  btnText: string;
}

interface Props {
  content: Content;
}

const ServicePurposeContent: React.FC<Props> = ({ content }) => {
  const { title, description, btnText } = content;
  return (
    <Fragment>
      {' '}
      <Typography variant="h3" color="inherit">
        {title}
      </Typography>
    </Fragment>
  );
};

export default ServicePurposeContent;
