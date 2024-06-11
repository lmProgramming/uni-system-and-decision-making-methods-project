using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;

public sealed class DataSaver : MonoBehaviour
{
    public static DataSaver instance;

    public int savesLeftToResetSimulation;
    public int timeIntervalToSave;
    int lastTimeSaved = 0;

    public string csvFolderName = "data";
    StringBuilder csv;
    StringBuilder csvInitialSettings;

    string currentCSVName = "0.csv";

    private void Awake()
    {
        instance = this;
    }

    string CsvsDataPath()
    {
        return Application.persistentDataPath + "/" + csvFolderName;
    }

    string CurrentCsvPath()
    {
        return CsvsDataPath() + "/" + currentCSVName;
    }

    public FileInfo[] GetFilesFromSaveLocation()
    {
        FileInfo[] fileInfo;
        try
        {
            DirectoryInfo info = new DirectoryInfo(CsvsDataPath());

            fileInfo = info.GetFiles();
        }
        catch
        {
            fileInfo = new FileInfo[0];
        }

        return fileInfo;
    }

    void Start()
    {
        CreateDataFolder();

        currentCSVName = $"Attempt {GetFilesFromSaveLocation().Length / 2} - {DateTime.Now.ToString("dd/MM/yyyy hh-mm-ss")}.csv";
        string initialcurrentCSVName = currentCSVName.Replace("Attempt", "Initial settings");

        lastTimeSaved = -timeIntervalToSave;

        csvInitialSettings = new StringBuilder();
        csv = new StringBuilder();

        csvInitialSettings.AppendLine("mapSize;startingCreatures;timeToSpawnAFood;hungerMult;speedMult;mitosisSpeedMult;mutationRange;bodyPartMutationChance;intervalBetweenBirths;hungerMultFromAge;newCellCreationCostMult;aggresivnesMult;genesCostMult;bodyPartsCostMult;initialSize;fullyRandomiseStartingGenes;allCreaturesStartAsDesignedCreature;startAsACreature;colorfulCells;speedGeneOn;sensorGeneOn;processingGeneOn;gluttonyGeneOn;reproductionGeneOn;storageGeneOn;parentEmpathyGeneOn;aggresivnessGeneOn;healthGeneOn;foodPreferenceGeneOn;fightingPermitted");

        csvInitialSettings.AppendLine($"{PlayerPrefs.GetFloat("mapSize")};{(int)PlayerPrefs.GetFloat("startingCreatures")};{1f / PlayerPrefs.GetFloat("timeToSpawnAFood")};{PlayerPrefs.GetFloat("hungerMult")};{PlayerPrefs.GetFloat("speedMult")};{PlayerPrefs.GetFloat("mitosisSpeedMult")};{PlayerPrefs.GetFloat("mutationRange")};{PlayerPrefs.GetFloat("bodyPartMutationChance")};{PlayerPrefs.GetFloat("intervalBetweenBirths")};{PlayerPrefs.GetFloat("hungerMultFromAge")};{PlayerPrefs.GetFloat("newCellCreationCostMult")};{PlayerPrefs.GetFloat("aggresivnesMult")};{PlayerPrefs.GetFloat("genesCostMult")};{PlayerPrefs.GetFloat("bodyPartsCostMult")};{PlayerPrefs.GetFloat("initialSize")};{PlayerPrefs.GetInt("fullyRandmoiseStartingGenes")};{PlayerPrefs.GetInt("allCreaturesStartAsDesignedCreature")};{PlayerPrefs.GetInt("startAsACreature")};{PlayerPrefs.GetInt("colorfulCells")};{PlayerPrefs.GetInt("speedGeneOn")};{PlayerPrefs.GetInt("sensorGeneOn")};{PlayerPrefs.GetInt("processingGeneOn")};{PlayerPrefs.GetInt("gluttonyGeneOn")};{PlayerPrefs.GetInt("reproductionGeneOn")};{PlayerPrefs.GetInt("storageGeneOn")};{PlayerPrefs.GetInt("parentEmpathyGeneOn")};{PlayerPrefs.GetInt("aggresivnessGeneOn")};{PlayerPrefs.GetInt("healthGeneOn")};{PlayerPrefs.GetInt("foodPreferenceGeneOn")};{PlayerPrefs.GetInt("fightingPermitted")}");

        File.WriteAllText(CsvsDataPath() + "/" + initialcurrentCSVName, csvInitialSettings.ToString());

        csv.AppendLine("simulation time;speed gene;sensor gene;processing gene;gluttony gene;reproduction wilness gene;energy storage capacity gene;parental empathy gene;aggresivness gene;health gene;food preference gene;creatures count;average creature cost;average amount of body parts;average amount of protective spikes;average amount of composters;average amount of turbines;average amount of offensive spikes;");

        Debug.Log(CurrentCsvPath());
    }

    public void CreateDataFolder()
    {
        string filePath = CsvsDataPath();

        if (!Directory.Exists(filePath))
        {
            Directory.CreateDirectory(filePath);
        }
    }

    public static string JoinWithComma(params object[] values)
    {
        return string.Join(", ", values);
    }

    void Update()
    {
        if (lastTimeSaved + timeIntervalToSave <= GameManager.Instance.simulationTime)
        {
            lastTimeSaved += timeIntervalToSave;

            GameManager g = GameManager.Instance;

            List<List<float>> values = g.valuesByTime;

            List<float> valuesToSave = new List<float>();

            for (int i = 0; i < values.Count; i++)
            {
                valuesToSave.Add(values[i][^1]);
            }

            csv.AppendLine($"{g.simulationTime};{string.Join(";", valuesToSave)}");

            savesLeftToResetSimulation--;

            if (savesLeftToResetSimulation <= 0)
            {
                End();
            }
        }
    }

    public void End(string additionalMessage="")
    {
        if (additionalMessage != "") 
        {
            csv.AppendLine(additionalMessage);
        }

        SaveData();
        SceneLoader.Instance.MainGame();
    }

    void SaveData()
    {
        File.WriteAllText(CurrentCsvPath(), csv.ToString());

        Debug.Log(CurrentCsvPath());
    }

    void OnApplicationQuit()
    {
        SaveData();
    }
}
