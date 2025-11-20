using System;

namespace StringUtilitiesApp
{
    public static class StringUtils
    {
        public static bool IsPalindrome(string input)
        {
            if (string.IsNullOrWhiteSpace(input)) return false;
            string normalized = input.Replace(" ", "").ToLower();
            char[] arr = normalized.ToCharArray();
            Array.Reverse(arr);
            return normalized == new string(arr);
        }

        public static string ReverseWords(string input)
        {
            if (string.IsNullOrWhiteSpace(input)) return input;
            string[] words = input.Split(' ');
            Array.Reverse(words);
            return string.Join(" ", words);
        }

        public static int CountVowels(string input)
        {
            if (string.IsNullOrWhiteSpace(input)) return 0;
            int count = 0;
            foreach (char c in input.ToLower())
            {
                if ("aeiou".Contains(c))
                {
                    count++;
                }
            }
            return count;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            string test = "Madam";

            Console.WriteLine($"Is '{test}' a palindrome? {StringUtils.IsPalindrome(test)}");

            string sentence = "The quick brown fox";
            Console.WriteLine($"Reversed words: {StringUtils.ReverseWords(sentence)}");

            string text = "OpenAI Documentation Generator";
            Console.WriteLine($"Vowel count: {StringUtils.CountVowels(text)}");
        }
    }
}
