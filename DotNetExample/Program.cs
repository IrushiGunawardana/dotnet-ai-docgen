using System;

namespace CalculatorApp
{
    public class Calculator
    {
        // Adds two numbers and returns the result
        public int Add(int a, int b)
        {
            return a + b;
        }

        // Subtracts b from a
        public int Subtract(int a, int b)
        {
            return a - b;
        }

        // Multiplies two numbers
        public int Multiply(int a, int b)
        {
            return a * b;
        }

        // Divides a by b
        public double Divide(int a, int b)
        {
            if (b == 0)
            {
                throw new DivideByZeroException("Cannot divide by zero.");
            }

            return (double)a / b;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Calculator calc = new Calculator();
            Console.WriteLine("Add: " + calc.Add(10, 5));
            Console.WriteLine("Subtract: " + calc.Subtract(10, 5));
            Console.WriteLine("Multiply: " + calc.Multiply(10, 5));
            Console.WriteLine("Divide: " + calc.Divide(10, 5));
        }
    }
}
