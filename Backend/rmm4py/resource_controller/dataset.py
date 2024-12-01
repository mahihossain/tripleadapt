"""
Class provides an overview over the different available datasets and their properties
"""

from enum import Enum
from tqdm import tqdm
import os
import pandas as pd
import rmm4py.models.importer.bpmn_importer as bpmn_importer
import rmm4py.models.importer.epc_importer as epc_importer
import rmm4py.models.importer.petrinet_importer as petrinet_importer
import rmm4py.models.importer.json_importer as json_importer
from rmm4py.event_logs.importer.csv_importer import load_csv_log
from rmm4py.event_logs.importer.xes_importer import import_xes
import requests
import rmm4py.resource_controller.path_helper as ph
import rmm4py.resource_controller.file_extractor as fe
import filecmp
import shutil

# global dictionary containing a tuple of the Modeltype and file extension as key and the Importer method as the value.


_FORMATS = {
    ("BPMN", "bpmn"): bpmn_importer.load_diagram_from_xml,
    ("EPC", "epml"): epc_importer.load_diagram_from_epml,
    ("PETRINET", "pnml"): petrinet_importer.load_diagram_from_pnml,
    ("OTHER", "csv"): pd.read_csv,
    ("EVENT_LOG", "xes"): import_xes,
    ("EVENT_LOG", "csv"): load_csv_log,
    ("JSON", "json"): json_importer.load_diagram_from_json,
}

ROOT_DIR = os.path.split(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))[0]
MSG_DECOMPRESS_FAILED = "Decompression failed."


class Modeltypes(Enum):
    """
    Enum for different Types of Models
    """
    BPMN = "BPMN"
    EPC = "EPC"
    EVENT_LOG = "EVENT_LOG"
    PETRINET = "PETRINET"


class DatasetCollection(Enum):
    """
    Enum for datasets.
    The additional key "dir" indicates when a file is a directory.
    """

    """Logs"""
    XES_STANDARD_LOGS = {
        "link": "https://www.win.tue.nl/ieeetfpm/lib/exe/fetch.php?media=shared:downloads:xes_certification_import_logs.zip",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "XES_Import_Certificate"),
        "filename": "XES certification import logs.zip"
    }

    BPIC2012 = {
        "link": "https://www.win.tue.nl/bpi/lib/exe/fetch.php?media=2012:financial_log.xes.gz",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2012"),
        "filename": "financial_log.xes.gz"
    }

    BPIC2013_COMPLETE = {
        "link": "https://www.win.tue.nl/bpi/lib/exe/fetch.php?media=2013:bpi_challenge_2013_incidents.xes.gz",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2013"),
        "filename": "bpi_challenge_incidents.xes.gz"
    }

    BPIC2013_OPEN = {
        "link": "https://www.win.tue.nl/bpi/lib/exe/fetch.php?media=2013:bpi_challenge_2013_open_problems.xes.gz",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2013"),
        "filename": "bpi_challenge_2013_open_problems.xes.gz"
    }

    BPIC2013_CLOSED = {
        "link": "https://www.win.tue.nl/bpi/lib/exe/fetch.php?media=2013:bpi_challenge_2013_closed_problems.xes.gz",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2013"),
        "filename": "bpi_challenge_2013_closed_problems.xes.gz"
    }

    BPIC2013_CSV = {
        "link": "https://www.win.tue.nl/bpi/lib/exe/fetch.php?media=2013:csv_files.zip",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2013"),
        "filename": "csv_files.zip",
        "dir": True
    }

    BPIC2015_1 = {
        "link": "https://data.4tu.nl/ndownloader/files/24063818",
        "model_type": "EVENT_LOG", "destination_dir":
        os.path.join("event_logs", "BPIC_2015"),
        "filename": "BPIC15_1.xes"
    }

    BPIC2015_2 = {
        "link": "https://data.4tu.nl/ndownloader/files/24044639",
        "model_type": "EVENT_LOG", "destination_dir":
        os.path.join("event_logs", "BPIC_2015"),
        "filename": "BPIC15_2.xes"
    }

    BPIC2015_3 = {
        "link": "https://data.4tu.nl/ndownloader/files/24076154",
        "model_type": "EVENT_LOG", "destination_dir":
        os.path.join("event_logs", "BPIC_2015"),
        "filename": "BPIC15_3.xes"
    }

    BPIC2015_4 = {
        "link": "https://data.4tu.nl/ndownloader/files/24045332",
        "model_type": "EVENT_LOG", "destination_dir":
        os.path.join("event_logs", "BPIC_2015"),
        "filename": "BPIC15_4.xes"
    }

    BPIC2015_5 = {
        "link": "https://data.4tu.nl/ndownloader/files/24069341",
        "model_type": "EVENT_LOG", "destination_dir":
        os.path.join("event_logs", "BPIC_2015"),
        "filename": "BPIC15_5.xes"
    }

    BPIC2016_NOT_LOGGED_IN = {
        "link": "https://data.4tu.nl/ndownloader/files/24063158",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2016"),
        "filename": "BPI2016_Clicks_NOT_Logged_In.csv.zip",
        "dir": True
    }

    BPIC2016_LOGGED_IN = {
        "link": "https://data.4tu.nl/ndownloader/files/23991602",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2016"),
        "filename": "BPI2016_Clicks_Logged_In.csv.zip",
        "dir": True
    }

    BPIC2017 = {
        "link": "https://data.4tu.nl/ndownloader/files/24044117",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2017"),
        "filename": "bpic_2017.xes.gz"
    }

    BPIC2018 = {
        "link": "https://data.4tu.nl/ndownloader/files/24025820",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2018"),
        "filename": "bpi_challenge_2018.xes.gz"
    }

    BPIC2019 = {
        "link": "https://data.4tu.nl/ndownloader/files/24072995",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2019"),
        "filename": "BPI_Challenge_2019.xes"
    }

    BPIC2020_DOMESTIC_DECLARATIONS = {
        "link": "https://data.4tu.nl/ndownloader/files/24031811",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2020"),
        "filename": "DomesticDeclarations.xes.gz"
    }

    BPIC2020_INTERNATIONAL_DECLARATIONS = {
        "link": "https://data.4tu.nl/ndownloader/files/24023492",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2020"),
        "filename": "InternationalDeclarations.xes.gz"
    }

    BPIC2020_PERMIT = {
        "link": "https://data.4tu.nl/ndownloader/files/24075929",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2020"),
        "filename": "PermitLog.xes.gz"
    }

    BPIC2020_PREPAID_TRAVEL_COSTS = {
        "link": "https://data.4tu.nl/ndownloader/files/24043835",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2020"),
        "filename": "PrepaidTravelCost.xes.gz"
    }

    BPIC2020_REQUEST_FOR_PAYMENT = {
        "link": "https://data.4tu.nl/ndownloader/files/24061154",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "BPIC_2020"),
        "filename": "RequestForPayment.xes.gz"
    }

    HELPDESK = {
        "link": "https://data.mendeley.com/public-files/datasets/39bp3vv62t/files/20b5d03f-c6f7-4fdc-91c3-67defd4c67bb/file_downloaded",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "Helpdesk"),
        "filename": "helpdesk.csv"
    }

    MOBIS_2019_CSV = {
        "link": "http://134.96.72.81/mobis_challenge_log_2019.csv",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "MobisChallenge2019"),
        "filename": "mobis_challenge_log_2019.csv"
    }

    MOBIS_2019_XES = {
        "link": "http://134.96.72.81/mobis_challenge_log_2019.xes",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "MobisChallenge2019"),
        "filename": "mobis_challenge_log_2019.xes"
    }

    PRODUCTION = {
        "link": "https://data.4tu.nl/ndownloader/files/24045434",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "Production"),
        "filename": "data.zip",
        "dir": True
    }

    RECHNUNGSVERARBEITUNG = {
        "link": "http://134.96.72.81/event_logs/Rechnungsverarbeitung/Rechnungsverarbeitungsprozess.xes",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "Rechnungsverarbeitung"),
        "filename": "Rechnungsverarbeitungsprozess.xes"
    }


    """Process Discovery Challenge"""
    PDC_2020_TRAIN = {
        "link": "https://data.4tu.nl/ndownloader/files/28090389",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "PDC", "2020"),
        "filename": "Training Logs.zip",
    }

    PDC_2020_TEST = {
        "link": "https://data.4tu.nl/ndownloader/files/28090392",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "PDC", "2020"),
        "filename": "Test Logs.zip",
    }

    PDC_2020_GT = {
        "link": "https://data.4tu.nl/ndownloader/files/28090395",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "PDC", "2020"),
        "filename": "Ground Truth Logs.zip",
    }


    """Synthetic event logs"""
    CAISE2022_EXP_1 = {
        "link": "http://134.96.72.81/CAISE_experiment_1.xes",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "synthetic", "simple_concurrency"),
        "filename": "CAISE_experiment_1.xes"
    }

    CAISE2022_EXP_2 = {
        "link": "http://134.96.72.81/CAISE_experiment_2.xes",
        "model_type": "EVENT_LOG",
        "destination_dir": os.path.join("event_logs", "synthetic", "simple_context"),
        "filename": "CAISE_experiment_2.xes"
    }

    """Models"""
    ADMISSION = {
        "link": "http://134.96.72.81/Admission.epml",
        "model_type": "EPC",
        "destination_dir": os.path.join("models", "Admission"),
        "filename": "admission.epml"
    }

    MOHOL_DE = {
        "link": "http://134.96.72.81/MoHoL_komplett_DE.zip",
        "model_type": "EPC",
        #"destination_dir": os.path.join("models", "MoHoL_DE"),
        "destination_dir": os.path.join("models", "MoHoL_DE"),
        "filename": "MoHoL_komplett_DE.zip",
        "dir": True
    }

    MOHOL_EN = {
        "link": "http://134.96.72.81/MoHoL_komplett_EN.zip",
        "model_type": "EPC",
        "destination_dir": os.path.join("models", "MoHoL_EN"),
        "filename": "MoHoL_komplett_EN.zip",
        "dir": True
    }

    CAMUNDA = {
        "link": "https://github.com/camunda/bpmn-for-research/archive/master.zip",
        "model_type": "BPMN",
        "destination_dir": os.path.join("models", "camunda"),
        "filename": "master.zip",
        "dir": True
    }

    EXAMS = {
        "link": "http://134.96.72.81/Exams.epml",
        "model_type": "EPC",
        "destination_dir": os.path.join("models", "Exams"),
        "filename": "exams.epml"
    }

    PDC_2020_Models = {
        "link": "https://data.4tu.nl/ndownloader/files/28090398",
        "model_type": "Petri-Net",
        "destination_dir": os.path.join("models", "PDC", "2020"),
        "filename": "Models.zip"
    }

    BLOEMEN = {
        "link": "https://data.4tu.nl/ndownloader/files/24065333",
        "model_type": "Petri-Net",
        "destination_dir": os.path.join("models", "Bloemen"),
        "filename": "data.zip",
        "dir": True
    }


class Dataset:
    """
    Holds dataset specific properties
    """

    def __init__(self, folder_path, model_type):
        """
        Initiaties a dataset object with path, name, model_type, a list of model files, children, corresponding
        to subfolders and an alive flag, to indicate if the dataset is empty or not.

        Parameters
        ----------
        folder_path : str
            Path to the directory with the files that should be contained in the dataset.
            Also applicable for a single file.
        model_type : str
        """

        self.path = folder_path
        self.name = ""
        self.model_type = model_type
        self.models = []
        self.children = []

        self.build()

    def build(self):
        """
        Recursively builds the datasets: generates values for cls.models and cls.children

        Returns
        -------
        None
        """
        name_as_string = str(self.path)
        name = name_as_string.split(os.sep)[-1]
        self.name = replace_chars(name)
        try:
            with os.scandir(self.path) as content:
                for chunk in content:
                    if chunk.is_dir() and not str(chunk.name).startswith("."):
                        child_ds = Dataset(chunk.path, self.model_type)
                        self.add_child(child_ds)
                    elif chunk.is_file() and not str(chunk.name).startswith("."):
                        ext = chunk.path.split(".")[-1]
                        # only files corresponding to the model_type are kept
                        if (self.model_type, ext) in _FORMATS:
                            self.models.append(chunk.path)

        # in case we have a single file (like in helpdesk dataset)
        except NotADirectoryError:
            self.models = [self.path]

    def add_child(self, dataset):
        """
        Adds a dataset to the list of children of an object and dynamically instantiates the attribute

        Parameters
        ----------
        dataset : Dataset

        Returns
        -------
        None
        """
        if not dataset.models and not dataset.children:
            return

        self.children.append(dataset)
        setattr(self, dataset.name, dataset)

    def load(self, recursive=True, **kwargs):
        """
        Function returns internal representation (networkx.DiGraph or petrinet), based on file extension within
        directory

        Returns
        -------
        list of CollaborationModel or petrinets
        """

        representation = []

        for model in self.models:
            ext = model.split(".")[-1]
            key = (self.model_type, ext)
            representation.append(_FORMATS[key](model, **kwargs))

        if recursive:
            for dataset in self.children:
                child_rep = dataset.load()
                try:
                    representation.extend(child_rep)
                # TypeError will occur, in case only one model is returned.
                except TypeError:
                    representation.append(child_rep)

        if len(representation) == 1:
            return representation[0]

        return representation

    def get_path(self):
        """
        Returns the path to the folder the dataset is based on.

        Returns
        -------
        path : str
        """

        return self.path

    def get_children(self):
        """
        Functions returns a list of all children dataset objects (subfolders).

        Returns
        -------
        list of Dataset
        """

        return self.children

    def info(self, last=[]):
        """
        Method prints out the tree structure of the dataset

        Parameters
        ----------
        last : list of bool

        Returns
        -------

        """
        prefix = ""
        for boolean in last[:-1]:
            if boolean:
                prefix += "   "
            else:
                prefix += "|  "

        if not last:
            print(self.name)
        elif last[-1]:
            print(prefix + "'--" + self.name)
        else:
            print(prefix + "|--" + self.name)

        for child in self.children:
            if child == self.children[-1]:
                _last = last.copy()
                _last.append(True)
                child.info(_last)

            else:
                _last = last.copy()
                _last.append(False)
                child.info(_last)


def datasets_overview():
    """
    Function prints all Datasets contained in the Datasets.ENUM

    Returns
    -------
    None
    """
    for dataset in DatasetCollection:
        print(dataset)


def replace_chars(string):
    """
    Replaces characters in a string which have potential function in python (such as - or +) with uncritical ones.

    Parameters
    ----------
    string : str

    Returns
    -------
    str
    """
    letters = {" ": "_", "-": "_", "+": "_"}
    new_string = string
    for letter in letters:
        new_string = new_string.replace(letter, letters[letter])
    return "DS_" + new_string


def download_any_format(url, file_name=None, dest_dir=None, compressed=False):
    """
    Downloads any file to the given directory and sets filename to file_name. Decompresses if compressed=True.

    Parameters
    ----------
    url : str
    dest_dir : str
        complete path to location
    file_name : str
        Name of the file or folder that will be downloaded, including the extension of the file.
    compressed : bool, optional
        If True, folder is decompressed automatically. The extraction method is based on the extension of
        file_name, e.g. "xyz.zip"

    Returns
    -------
    Path.Posix
    """

    if file_name is None:
        file_name = url.split("/")[-1]

    if dest_dir is None:
        dest_dir = ph.get_folder_path(ph.Folder.DATA)

    print(f"Downloading {file_name}")
    print(url)
    # previously model_download(url, _dest_dir)
    # if the destination directory does not exists yet, it is created
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # download
    file_path = os.path.join(dest_dir, file_name)
    # remove files at that location if already exist
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)

    elif os.path.exists(file_path) and os.path.isdir(file_path):
        raise IsADirectoryError

    download = requests.get(url, stream=False)
    filesize = int(download.headers.get('content-length', 0))
    if download.ok:
        print("file is being saved to path", os.path.abspath(file_path))
        try:
            with open(file_path, 'wb') as file, tqdm(unit="B", unit_scale=True, unit_divisor=1024, total=filesize,
                                                     desc=file_path) as progress:
                for chunk in download.iter_content(chunk_size=1024 * 8):
                    # if chunk:
                    file.write(chunk)
                    file.flush()
                    os.fsync(file.fileno())
                    progress.update(len(chunk))

        except IsADirectoryError:
            raise IsADirectoryError

    else:
        # HTTP status code 4XX/5XX
        print(f"Download failed: status code {download.status_code}\n{download.text}")
        return

    print("File downloaded successfully")

    if compressed:
        try:
            extraction_method = fe.find_extractor(file_name)
            extraction_method(dest_dir)
            print("File decompressed successfully")

        except NotImplementedError:
            raise NotImplementedError("Directory was not decompressed successfully.")


def __checksum_check(url, path, compressed=False):
    """
    Function checks whether the remote file and the local copy have the same checksum by comparing the remote md5 with
    the md5 saved in "checksum.txt" file which is generated automatically upon extraction.

    Parameters
    ----------
    url : str
        url to remote file
    path : str
        path to local (compressed) file
    compressed : bool

    Returns
    -------
    bool
        True if checksums are equal, False otherwise
    """

    # In a first step the checksums of the (compressed) file on the server and the local (compressed) file are compared.
    # If the files are not compressed, no further step is needed, the result is returned immediately.
    # If the files are compressed, the program checks for local changes. The compressed file is decompressed again
    # and then compared against the local version of the decompressed folder.

    if not compressed:
        checksum_remote = fe.md_5_remote_checksum(url)
        checksum_local = fe.md_5_checksum(path)
        return checksum_local == checksum_remote
    else:
        filename = path.split(os.sep)[-1]
        extraction_method = fe.find_extractor(filename)
        extraction_method(os.path.join(ph.get_folder_path(ph.Folder.DATA), "temp_dir"))
        temp_path = ph.look_for_directory("temp_dir")
        old_version = path.replace(os.sep+filename, "")
        dir_equal = __recursive_directory_comparison(temp_path, old_version)
        shutil.rmtree(temp_path)
        return dir_equal


def __recursive_directory_comparison(dir1, dir2):
    """
    Function compares files of two directories and returns False if any files have been modified or deleted, True if the
    dirs are identical.

    Parameters
    ----------
    dir1 : str
        Path to the first directory
    dir2 : str
        Path to the second directory

    Returns
    -------
    bool
    """

    common = []
    for chunk in os.scandir(dir1):
        if chunk.is_file():
            common.append(chunk.name)
        if chunk.is_dir():
            new_dir1 = chunk.path
            new_dir2 = os.path.join(dir2, chunk.name)
            dir_equal = __recursive_directory_comparison(new_dir1, new_dir2)
            if not dir_equal:
                return False

    match, mismatch, errors = filecmp.cmpfiles(dir1, dir2, common, shallow=False)

    if len(mismatch) >= 1 or len(errors) >= 1:
        print("These files have been modified locally (incomplete list):")
        print(mismatch)
        print("These files have been deleted locally (incomplete list):")
        print(errors)
        return False

    return True


def generate_dataset_from_url(dataset, typ, url, compressed, filename=None, only_path=False):
    """
    If the dataset is not contained in the Datasets.ENUM this function can be used to generate a dataset providing a
    url and a Modeltypes.ENUM. This method will always perform a download from the given url.
    In case you already downloaded a folder, you can create a Dataset object directly.
    Also consider to add the dataset to the Datasets.ENUM, if you use it frequently.

    Parameters
    ----------
    dataset : str
        name of the dataset, files will be stored in a folder with this name
    typ : Modeltypes.enum_member
        For any format of files, that have different interpretations (like .csv) it must be specified
        which type the files are
    url : str
        url to the dataset file
    compressed : bool
        set to True, if you are downloading a compressed file, false otherwise.
    filename : str, optional
        If the filename is not part of the url, it is recommended to provide it here.
        The extension of the filename will be used to determine the extraction method, if needed.
    only_path : bool, optional
        Defaults to false, a dataset is returned directly
        If true, just the path to the model-files is returned.

    Returns
    -------
    Dataset

    """
    if filename is None:
        filename = url.split("/")[-1]
    path = os.path.join(ph.get_folder_path(ph.Folder.DATA), dataset)
    # downloads by default
    download_any_format(url, filename, path, compressed)
    obj = os.scandir(path)
    for chunk in obj:
        if chunk.is_dir():
            obj.close()
            if only_path:
                return path
            else:
                return Dataset(path, typ.value)
        if chunk.name in filename:
            chunk_path = chunk.path
            obj.close()
            if only_path:
                return chunk_path
            else:
                return Dataset(chunk_path, typ.value)
    """
    else:
        if only_path:
            return path
        else:
            return Dataset(path, typ.value)
    """

def generate_dataset(dataset, only_path=False, force_update=False, check_updates=False):
    """
    Function loads models or subsets of models.

    Parameters
    ----------
    dataset : Datasets.enum_member
        member of the datasets enum
    only_path : bool, optional
        Defaults to false, a list of CollaborationModels is returned directly
        If true, just the path to the model-files is returned.
    force_update : bool, optional
        Defaults to false, if the directory already exists, it will not be downloaded again,
        unless check_updates requires this.
        If true, the current version of the directory will be overwritten
    check_updates : bool, optional
        Defaults to true, checksums are compared, to identify, if the version at the url and the
        locally saved one are the same.

    Returns
    -------
    list of CollaborationModel or other internal representation or list of str

    """

    dest_dir = dataset.value["destination_dir"]
    filename = dataset.value["filename"]
    path = os.path.join(ph.get_folder_path(ph.Folder.DATA), dest_dir)
    url = dataset.value["link"]
    typ = dataset.value["model_type"]
    # directories and single files need to be treated differently.
    folder = False
    if "dir" in dataset.value.keys():
        folder = True

    # determine the length of the extension and exclude it from the file_path, if it indicates compression
    # if compressed, also set parameter compressed to true.
    file_path_comp = os.path.join(path, filename)
    ext = os.path.splitext(filename)[-1]
    compressed = False
    if ext[1:] in fe.COMPRESSION_FORMATS:
        file_path = file_path_comp[:-len(ext)]
        compressed = True
    else:
        file_path = file_path_comp

    # executed if the folder or file exists and no updates are required.
    if (folder and os.path.exists(path) and not force_update and not check_updates) or \
            (os.path.exists(file_path) and not force_update and not check_updates):
        if only_path and folder:
            return path
        elif only_path and not folder:
            return file_path
        else:
            if folder:
                data = Dataset(path, typ)
            else:
                data = Dataset(file_path, typ)
            return data

    # executed if an update is forced or the folder or filepath does not exist yet.
    elif force_update or not os.path.exists(path) or not os.path.exists(file_path) and not folder:
        download_any_format(url, filename, path, compressed)

    # execute if we check for updates.
    else:
        if check_updates:
            temp_path = file_path
            if folder:
                temp_path = path
            if compressed:
                checksum_path = ph.hide_file(file_path_comp)
            else:
                checksum_path = file_path_comp

            checksums_equal = __checksum_check(url, checksum_path, compressed)
            if checksums_equal and not only_path:
                data = Dataset(str(temp_path), typ)
                return data
            elif checksums_equal and only_path:
                return temp_path
            else:
                download_any_format(url, filename, path, compressed)

    if only_path and folder:
        return path
    elif only_path and not folder:
        return file_path

    else:
        if folder:
            data = Dataset(str(path), typ)
            return data
        else:
            data = Dataset(str(file_path), typ)
            return data
