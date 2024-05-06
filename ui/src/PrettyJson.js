import React from 'react';

function PrettyJson({ data }) {
  // Convert the JSON data to a string with 2-space indentation
  const jsonString = JSON.stringify(data, null, 2);

  return (
    <pre>
      <code>{jsonString}</code>
    </pre>
  );
}

export default PrettyJson;