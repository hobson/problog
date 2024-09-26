import React from 'react';
import { Box, Typography } from '@mui/material';

const colorStyle = (colors: string[], color: string) => {
    return {
        backgroundColor: color,
        width: `${100 / colors.length}%`,
        height: '100%',
    };
}

interface ColorDiagramProps {
  colors: string[];
}

const ColorDiagram: React.FC<ColorDiagramProps> = ({ colors }) => {
  const sectionLabels = ['0', '.5', '1'];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" mb={1}>
        {sectionLabels.map((label, index) => (
          <Typography key={index} variant="body2" sx={{ textAlign: 'center', width: `${100 / sectionLabels.length}%`, fontFamily: 'Dosis', fontWeight: 500, fontSize: 18 }}>
            {label}
          </Typography>
        ))}
      </Box>

      <Box display="flex" width="100%" height="100px" sx={{ overflow: 'hidden', borderRadius: '8px' }}>
        {colors.map((color, index) => (
          <Box key={index} sx={colorStyle(colors, color)} />
        ))}
      </Box>
    </Box>
  );
};

export default ColorDiagram;
