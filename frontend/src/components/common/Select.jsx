// ============================================================================
// FILE: src/components/common/Select.jsx
// PURPOSE: Reusable select dropdown component
// ============================================================================

import React from 'react';

export const Select = ({
  label,
  name,
  value,
  onChange,
  onBlur,
  options,
  error,
  placeholder = 'Select...',
  required = false,
  disabled = false,
  className = '',
}) => {
  const handleChange = (e) => {
    onChange(name, e.target.value);
  };

  const handleBlur = () => {
    if (onBlur) {
      onBlur(name);
    }
  };

  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-medium text-purple-500 mb-2">
          {label}
          {required && <span className="text-red-400 ml-1">*</span>}
        </label>
      )}
      <select
        name={name}
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={disabled}
        required={required}
        className={`w-full px-4 py-3 bg-white/10 border ${
          error ? 'border-red-500' : 'border-white/20'
        } rounded-xl text-purple-200 focus:outline-none focus:ring-2 ${
          error ? 'focus:ring-red-400' : 'focus:ring-purple-400'
        } disabled:opacity-30 disabled:cursor-not-allowed`}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="mt-1 text-sm text-red-400">{error}</p>
      )}
    </div>
  );
};
