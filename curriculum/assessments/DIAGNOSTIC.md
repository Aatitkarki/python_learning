# Starting diagnostic

You selected the beginner path, so no prior knowledge is assumed. Try these for 30 minutes before studying; “I do not know yet” is useful information. Do not score yourself by whether a topic looks familiar.

1. Predict `3 + 2 * 4`, `"3" + "4"`, and `len([1, 1, 2])`.
2. Write a function returning the larger of two numbers. What happens if they are equal?
3. Count words in a sentence using a dictionary.
4. Explain why `0.1 + 0.2` may not equal exactly `0.3` in binary floating point.
5. For vectors [1,2] and [3,4], calculate the dot product. Can a 2×3 matrix multiply a 2×2 matrix?
6. Calculate mean and sample variance of [1,2,3]. Explain what variance measures.
7. Of 1,000 events, 10 are real alerts. A detector finds 9 and also flags 99 ordinary events. What is precision?
8. Explain why fitting a scaler on the whole dataset before a train/test split can leak information.
9. Explain authentication versus authorization with two users and a private document.
10. Describe how you would determine whether an AI answer’s citation actually supports its number.

Use the answers below only after attempting all ten. The original README checks Statistics; treat questions 6–7 as a quick recheck of that existing experience.

<details><summary>Answer key and routing</summary>

1. 11, the string "34", and 3. Operators have precedence, and string addition concatenates.
2. `return a if a >= b else b`; equal values return that same value.
3. Normalize/split according to a stated policy, then increment `counts[word] = counts.get(word, 0)+1`.
4. Many decimal fractions have no finite binary representation; use tolerances or decimal arithmetic according to the domain.
5. Dot product = 11. A 2×3 matrix cannot multiply a 2×2 matrix in that order because inner dimensions 3 and 2 differ.
6. Mean = 2; sample variance = 1. Population variance of those three observations = 2/3. Variance summarizes squared deviations from the mean.
7. Precision = 9/(9+99) = 1/12 ≈ 8.33%; recall = 9/10 = 90%. High recall does not imply high precision.
8. The scaler’s parameters would incorporate information from held-out observations. Fit it on training data or inside each cross-validation fold.
9. Authentication verifies identity; authorization checks whether that identity may access a specific document. A claimed tenant in a question does not establish identity.
10. Inspect the original source/version, identify the exact supporting span/table, verify units/period/calculation, and check permission. Merely linking to an existing document is insufficient.

Start at Stage 00 regardless. If questions 1–4 are difficult, use the full Stage 01 budget. If 5–7 are difficult, retain all Stage 02 practice. Familiarity with 8–10 does not justify skipping implementation gates.

</details>
