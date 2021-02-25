from django.db import models

# Create your models here.
class kampania_redlink(models.Model):
    nazwa_kampanii = models.CharField(max_length=100)
    kiedy_wyslany = models.CharField(max_length=100)
    temat_mailingu_pl = models.CharField(max_length=100)
    temat_mailingu_en = models.CharField(max_length=100)
    temat_mailingu_de = models.CharField(max_length=100)
    temat_mailingu_fr = models.CharField(max_length=100)
    redlink_id_a_sitek_pl = models.CharField(max_length=100)
    redlink_id_c_idziak_pl = models.CharField(max_length=100)
    redlink_id_i_rosinska_pl = models.CharField(max_length=100)
    redlink_id_m_mikolajczyk_pl = models.CharField(max_length=100)
    redlink_id_m_kluszczynska_pl = models.CharField(max_length=100)
    redlink_id_t_piszczola_pl = models.CharField(max_length=100)
    redlink_id_a_biegajlo_en = models.CharField(max_length=100)
    redlink_id_j_nieglos_en = models.CharField(max_length=100)
    redlink_id_l_urbanczyk_en = models.CharField(max_length=100)
    redlink_id_m_prange_en = models.CharField(max_length=100)
    redlink_id_m_bujakowska_en = models.CharField(max_length=100)
    redlink_id_p_strzelecki_en = models.CharField(max_length=100)
    redlink_id_l_urbanczyk_de = models.CharField(max_length=100)
    redlink_id_m_prange_de = models.CharField(max_length=100)
    redlink_id_m_bujakowska_de = models.CharField(max_length=100)
    redlink_id_a_biegajlo_fr = models.CharField(max_length=100)
    redlink_id_m_prange_fr = models.CharField(max_length=100)
    redlink_id_m_sobaszek_en = models.CharField(max_length=100)
    link_content = models.CharField(max_length=200)
    def __str__(self):
        return self.nazwa_kampanii