import React from 'react';
import { useStyles } from './styles';

export default function Footer() {
  const { footer } = useStyles();

  return <footer className={footer}>Footer</footer>;
}
