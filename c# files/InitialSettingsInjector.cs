using Newtonsoft.Json.Linq;
using UnityEngine;

public class InitialSettingsInjector : MonoBehaviour
{
    float meanWeightMultiplier = 1.0f;

    void Start()
    {
        meanWeightMultiplier = 2 * (1 - (Random.value * Random.value));

        meanWeightMultiplier *= 1 + Random.value;

        PlayerPrefs.SetFloat("mapSize", GenerateRandomValue(20, 100, 40));

        PlayerPrefs.SetFloat("startingCreatures", GenerateRandomValue(1, 60, 25));

        PlayerPrefs.SetFloat("timeToSpawnAFood", 1f / GenerateRandomValue(0.1f, 15, 4));

        PlayerPrefs.SetFloat("mutationRange", GenerateRandomValue(0.01f, 1f, 0.1f));

        PlayerPrefs.SetFloat("bodyPartMutationChance", GenerateRandomValue(0.005f, 1f, 0.05f));

        PlayerPrefs.SetFloat("intervalBetweenBirths", GenerateRandomValue(0, 100, 40));

        PlayerPrefs.SetFloat("hungerMultFromAge", GenerateRandomValue(0, 3f / 300f, 1f / 300f));

        PlayerPrefs.SetFloat("newCellCreationCostMult", 1);

        PlayerPrefs.SetFloat("aggresivnesMult", GenerateRandomValue(0, 5, 1));

        PlayerPrefs.SetFloat("genesCostMult", GenerateRandomValue(0, 5, 1));

        PlayerPrefs.SetFloat("bodyPartsCostMult", GenerateRandomValue(0, 5, 1));
    }

    float GenerateRandomValue(float min, float max, float mean)
    {
        float meanWeight = meanWeightMultiplier * Random.value;

        float x = (Random.value + .5f * meanWeight) / (1 + meanWeight);

        float value = CustomPowerFunction(x, min, max, mean);

        return value;
    }

    float CustomPowerFunction(float x, float min, float max, float mean)
    {
        float meanInterpolated = (mean - min) / (max - min);

        return Mathf.Pow(x, Mathf.Log(meanInterpolated, 0.5f)) * (max - min) + min;
    }
}
