// Get the current date and time in ISO format (YYYY-MM-DD)
export const getCurrentDate = () => new Date().toISOString().split("T")[0];
