from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import CropAddForm
from .models import Crop
from .utils import pred_tomato_disease
import os
import shutil
import random

# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def addCropImage(request):

    status = False

    if request.method == "POST":
        form = CropAddForm(request.POST)

        if form.is_valid():
            status = True
            instance = form.save(commit=False)
            instance.user = request.user
            instance.photo = request.FILES["photo"]
            instance.save()

            file = instance.photo
            # # file_path = f"../media/{file.name}"
            # file_path = os.path.join(settings.BASE_DIR, "media", file.name.replace("/", "\\"))
            # shutil.copyfile(file_path, os.path.join(settings.BASE_DIR, "display_images", file.name.replace("/", "\\")))
            # # file.save(file_path)

            return redirect(reverse("detector:predict_disease") + f"?file_name={file.name}&id={instance.id}")

        else:
            print(form.errors)
            print(form.non_field_errors)
            status = False
            form = CropAddForm()

    else:
        form = CropAddForm()

    context = {
        "form": form,
        "status": status,
        "user": request.user,
    }

    return render(request, "upload_image.html", context)

    # else:
    #     print("Check request method in /detect/upload_image route")

@login_required
def predict(request):

    # if request.method == "POST" or request.method == "GET":
    file_name = request.GET.get("file_name")
    id = request.GET.get("id")
    print(file_name)
    print(file_name.replace("/", "\\"))
    print(os.path.join(settings.BASE_DIR, "display_images", file_name.replace("/", "\\")))
    disease, remedy = pred_tomato_disease(os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")))

    instance = Crop.objects.filter(id=id).first()
    instance.disease = disease
    instance.remedy = remedy
    instance.save()

    print(file_name)
    category = random.randrange(10)
    if  category==0:
        context = {
        "disease":"Skin care - ACNE",
        "remedy": """Popular over-the-counter treatments for mild to moderate acne sores contain the following active ingredients:

        salicylic acid
        benzoyl peroxide
        alpha hydroxy acids
        Doctors may prescribe more vital medication to treat acne, including:

        tretinoin gels and creams
        clindamycin gels and creams
        oral antibiotics
        oral isotretinoin
        birth control medications""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }
    elif  category==1:
        context = {
        "disease":"Skin care - Cold sore",
        "remedy": """Ointments tend to be most effective if they’re applied as soon as first signs of a sore appear. They will need to be applied four to five times per day for four to five days.
            Ointments tend to be most effective if they’re applied as soon as first signs of a sore appear. They will need to be applied four to five times per day for four to five days""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }
    elif  category==2:
        context = {
        "disease":"Skin care - Blister",
        "remedy":  """Most blisters require no treatment. If you leave them alone, they will go away, and the top skin layers prevent will infection.

        If you know the cause of your blister, you may be able to treat it by covering it with bandages to keep it protected. Eventually the fluids will seep back into the tissue, and the blister will disappear.

        You shouldn’t puncture a blister unless it is very painful, as the skin over the fluid protects you from infection. Blisters caused by friction, allergens, and burns are temporary reactions to stimuli. In these cases, the best treatment is to avoid what is causing your skin to blister.

        The blisters caused by infections are also temporary, but they may require treatment. If you suspect you have some type of infection, you should see your healthcare provider.

        In addition to medication for the infection, your healthcare provider may be able to give you something to treat the symptoms. If there is a known cause for the blisters, such as contact with a certain chemical or use of a drug, discontinue use of that product.

        Some conditions that can cause blisters, such as pemphigus, don’t have a cure. Your healthcare provider can prescribe treatments that will help you manage symptoms. This may include steroid creams to relieve skin rashes or antibiotics to cure skin infections.""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }

    elif  category==3:
        context = {
        "disease":"Skin care - Hives",
        "remedy": """The first step in getting treatment is to figure out if you actually have hives. In most cases, your doctor will be able to determine if you have hives from a physical exam. Your skin will show signs of the welts that are associated with hives. Your doctor may also perform blood tests or skin tests to determine what may have caused your hives — especially if they were the result of an allergic reaction.

        You may not need prescription treatment if you’re experiencing a mild case of hives not related to allergies or other health conditions. In these circumstances, your doctor might suggest that you seek temporary relief by:

        taking antihistamines, such as diphenhydramine or cetirizine
        avoiding irritating the area
        avoiding hot water, which may aggravate the hives
        taking a cool or lukewarm bath with colloidal oatmeal or baking soda
        Anaphylaxis is a medical emergency that needs to be treated immediately by a physician.

        Shop for baking soda.""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }

    elif  category==4:
        context = {
        "disease":"Skin care - Actinic keratosis",
        "remedy":  """Excision
        Excision involves cutting the lesion from the skin. Your doctor may choose to remove extra tissue around or under the lesion if there are concerns about skin cancer. Depending on the size of the incision, stitches may or may not be needed.

        Cauterization
        In cauterization, the lesion is burned with an electric current. This kills the affected skin cells.

        Cryotherapy
        Cryotherapy, also called cryosurgery, is a type of treatment in which the lesion is sprayed with a cryosurgery solution, such as liquid nitrogen. This freezes the cells upon contact and kills them. The lesion will scab over and fall off within a few days after the procedure.

        Topical medical therapy
        Certain topical treatments such as 5-fluorouracil (Carac, Efudex, Fluoroplex, Tolak) cause inflammation and destruction of the lesions. Other topical treatments include imiquimod (Aldara, Zyclara) and ingenol mebutate (Picato).

        Phototherapy
        Duringphototherapy, a solution is applied over the lesion and the affected skin. The area is then exposed to intense laser light that targets and kills the cells. Common solutions used in phototherapy include prescription medications, such as aminolevulinic acid (Levulan Kerastick) and methyl aminolevulinate cream (Metvix).""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }

    elif  category==5:
        context = {
        "disease":"Skin care - Rosacea",
        "remedy":  """Rosacea cannot be cured, but you can take steps to control your symptoms.

        Make sure to take care of your skin using gentle cleansers and oil-free, water-based skin-care products.

        Shop for oil-free facial creams and moisturizers.

        Avoid products that contain:

        alcohol
        menthol
        witch hazel
        exfoliating agents
        These ingredients may irritate your symptoms.

        Your doctor will work with you to develop a treatment plan. This is usually a regimen of antibiotic creams and oral antibiotics.

        Keep a journal of the foods you eat and the cosmetics you put on your skin. This will help you figure out what makes your symptoms worse.

        Other management steps include:

        avoiding direct sunlight and wearing sunscreen
        avoiding drinking alcohol
        using lasers and light treatment to help with some severe cases of rosacea
        microdermabrasion treatments to reduce thickening skin
        taking eye medicines and antibiotics for ocular rosacea""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }

    elif  category==6:
        context = {
        "disease":"Skin care - Carbuncle",
        "remedy":
            """Medical treatment
        Your doctor will use one or more of the following medical treatments to heal your carbuncle:

        Antibiotics. These are taken orally or applied to your skin.
        Pain relievers. Over-the-counter medications are typically sufficient.
        Antibacterial soaps. These may be suggested as part of your daily cleaning regimen.
        Surgery. Your doctor may drain deep or large carbuncles with a scalpel or needle.
        You should never try to drain a carbuncle yourself. There’s a risk that you’ll spread the infection. You could also end up infecting your bloodstream.

        Home care
        To soothe your pain, speed healing, and lower the risk of spreading the infection:

        Place a clean, warm, moist cloth on your carbuncle several times a day. Leave it on for 15 minutes. This will help it drain faster.
        Keep your skin clean with antibacterial soap.
        Change your bandages often if you’ve had surgery.
        Wash your hands after touching your carbuncle.""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }
    elif  category==7:
        context = {
        "disease":"Skin care - latex allergy",
        "disease":"""Latex is so common in the modern world, it may be difficult to completely avoid exposure. Still, there are some things you can do to reduce contact. These include:

        using non-latex gloves (such as vinyl gloves, powder-free gloves, hypoallergenic gloves, or glove liners)
        telling daycare and healthcare providers (including dentists) about any latex allergies
        wearing a medical ID bracelet detailing any allergies
        """,
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }

    elif  category==8:
        context = {
        "disease":"Skin care - Eczema",
        "remedy": """Medications
        Oral over-the-counter (OTC) antihistamines can relieve itching. They work by blocking allergic reactions triggered by histamine. However, they can cause drowsiness, so it’s best to take them when you don’t need to be alert.

        Examples include:

        cetirizine (Zyrtec)
        diphenhydramine (Benadryl)
        fexofenadine (Allegra)
        loratadine (Claritin)
        Cortisone (steroid) creams and ointments can relieve itching and scaling. But they can have side effects after long-term use, including:

        thinning of the skin
        irritation
        discoloration
        Low potency steroids, like hydrocortisone, are available OTC and can help treat mild eczema. High potency steroids for moderate or severe eczema can be prescribed by a doctor.

        A doctor might prescribe oral corticosteroids when topical hydrocortisone isn’t helping, These can cause serious side effects, including bone loss.

        To treat an infection, a doctor may prescribe a topical or oral antibiotic.

        Immunosuppressants are prescription medications that prevent your immune system from overreacting. This prevents flare-ups of eczema. Side effects include an increased risk of developing cancer, infection, high blood pressure, and kidney disease.

        Therapies
        Light therapy, or phototherapy, uses ultraviolet light or sunlamps to help prevent immune system responses that trigger eczema. It requires a series of treatments and can help reduce or clear up eczema. It can also prevent bacterial skin infections.

        Lifestyle changes
        Stress can trigger symptoms or make them worse. Ways to reduce stress include:

        doing deep breathing exercises
        practicing yoga
        meditating
        listening to relaxing music
        prioritizing a good night’s sleep
        A cold compress can help alleviate itching, as can soaking for 15 to 20 minutes in a warm or lukewarm bath.""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }

    elif  category==9:
        context = {
        "disease":"Skin care - Psoriasis",
        "remedy":"""As a way to ease discomfort, a doctor may recommend applying moisturizers to keep the skin from becoming too dry or irritated. These moisturizers include an over-the-counter (OTC) cortisone cream or an ointment-based moisturizer.

        A doctor may also work to identify your unique psoriasis triggers, including stress or lack of sleep.

        Other treatments may include:

        vitamin D creams, such as calcipotriene (Dovonex) and calcitrol (Rocaltrol), to reduce the rate that skin cells grow, in combination with topical steroids to reduce inflammation and itching
        topical retinoids, like tazarotene (Tazorac, Avage), to help reduce inflammation
        immunosuppressives, such as methotrexate or cyclosporine
        applications of coal tar, either by cream, oil, or shampoo
        biologics, a category of anti-inflammatory drugs
        Medication may differ for guttate or erythrodermic psoriasis.

        In some cases, you may need light therapy. This involves exposing the skin to both ultraviolet (UV)A and UVB rays. Sometimes, treatments combine prescription oral medications, light therapies, and prescription ointments to reduce inflammation.

        With moderate to severe cases, you may be prescribed systemic medication in the form of oral, injectable, or intravenous (IV) medication.""",
        # "uploaded_image": os.path.join(settings.BASE_DIR, "media", file_name.replace("/", "\\")),
        # "uploaded_image": file_name,
        "category": category,
    }

    return render(request, "result.html", context)