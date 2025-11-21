// ============================================================================
// FILE: src/components/common/Input.jsx
// PURPOSE: Reusable input component with light/dark mode support
// ============================================================================

import React from 'react';

export const Input = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  placeholder,
  required = false,
  disabled = false,
  min,
  max,
  className = '',
  ...props
}) => {
  const handleChange = (e) => {
    onChange(name, e.target.value);
  };

  const handleBlur = () => {
    if (onBlur) onBlur(name);
  };

  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-medium text-purple-500 mb-2">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <input
        type={type}
        name={name}
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={placeholder}
        disabled={disabled}
        min={min}
        max={max}
        required={required}
        className={`w-full px-4 py-3 
          bg-white border border-gray-300 text-gray-800 placeholder-gray-400
          rounded-xl shadow-sm
          focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500
          dark:bg-white/10 dark:border-white/20 dark:text-white dark:placeholder-purple-300/50
          disabled:opacity-50 disabled:cursor-not-allowed !bg-white !text-gray-800
          ${error ? 'border-red-500 focus:ring-red-400' : ''}
        `}
        {...props}
      />

      {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
    </div>
  );
};
