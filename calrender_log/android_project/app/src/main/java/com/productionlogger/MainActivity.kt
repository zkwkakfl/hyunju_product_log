package com.productionlogger

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.productionlogger.data.ModelInfo
import com.productionlogger.data.ProductionDatabase
import com.productionlogger.data.ProductionRecord
import com.productionlogger.databinding.ActivityMainBinding
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

/**
 * 메인 액티비티
 * 생산 기록 입력 및 메뉴 화면을 제공합니다.
 */
class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private lateinit var database: ProductionDatabase
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        // 데이터베이스 초기화
        database = ProductionDatabase.getDatabase(this)
        
        // 기본 모델 데이터 초기화
        initializeDefaultModels()
        
        // 오늘 날짜로 설정
        val today = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
        binding.editDate.setText(today)
        
        // 버튼 클릭 리스너 설정
        setupClickListeners()
    }
    
    private fun setupClickListeners() {
        // 저장 버튼
        binding.btnSave.setOnClickListener {
            saveProductionRecord()
        }
        
        // 달력 보기 버튼
        binding.btnCalendar.setOnClickListener {
            startActivity(Intent(this, CalendarActivity::class.java))
        }
        
        // 통계 보기 버튼
        binding.btnStatistics.setOnClickListener {
            startActivity(Intent(this, StatisticsActivity::class.java))
        }
        
        // 모델 관리 버튼
        binding.btnModelManagement.setOnClickListener {
            startActivity(Intent(this, ModelManagementActivity::class.java))
        }
        
        // 데이터 내보내기 버튼
        binding.btnExport.setOnClickListener {
            startActivity(Intent(this, ExportActivity::class.java))
        }
    }
    
    private fun saveProductionRecord() {
        val date = binding.editDate.text.toString().trim()
        val model = binding.editModel.text.toString().trim().uppercase()
        val quantityText = binding.editQuantity.text.toString().trim()
        
        // 입력 검증
        if (date.isEmpty() || model.isEmpty() || quantityText.isEmpty()) {
            showToast("모든 항목을 입력해주세요.")
            return
        }
        
        val quantity = try {
            quantityText.toInt()
        } catch (e: NumberFormatException) {
            showToast("수량은 숫자여야 합니다.")
            return
        }
        
        if (quantity <= 0) {
            showToast("수량은 0보다 커야 합니다.")
            return
        }
        
        // 날짜 형식 검증
        if (!isValidDate(date)) {
            showToast("날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)")
            return
        }
        
        // 모델 존재 여부 확인 및 단가 조회
        lifecycleScope.launch {
            val modelInfo = database.productionDao().getModelByName(model)
            if (modelInfo == null) {
                runOnUiThread {
                    showToast("'$model' 모델이 등록되지 않았습니다.")
                }
                return@launch
            }
            
            val amount = modelInfo.unitPrice * quantity
            
            val record = ProductionRecord(
                date = date,
                model = model,
                quantity = quantity,
                unitPrice = modelInfo.unitPrice,
                amount = amount
            )
            
            try {
                database.productionDao().insertRecord(record)
                runOnUiThread {
                    showToast("저장 완료! 금액: ${String.format("%,d", amount)}원")
                    // 입력 필드 초기화
                    binding.editModel.setText("")
                    binding.editQuantity.setText("")
                }
            } catch (e: Exception) {
                runOnUiThread {
                    showToast("저장 중 오류가 발생했습니다: ${e.message}")
                }
            }
        }
    }
    
    private fun initializeDefaultModels() {
        lifecycleScope.launch {
            val defaultModels = listOf(
                ModelInfo("MODEL-A", 1500, "MODEL-A 모델"),
                ModelInfo("MODEL-B", 2200, "MODEL-B 모델"),
                ModelInfo("MODEL-C", 1850, "MODEL-C 모델"),
                ModelInfo("MODEL-D", 3100, "MODEL-D 모델")
            )
            
            for (model in defaultModels) {
                try {
                    database.productionDao().insertModel(model)
                } catch (e: Exception) {
                    // 이미 존재하는 모델은 무시
                }
            }
        }
    }
    
    private fun isValidDate(dateString: String): Boolean {
        return try {
            val format = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
            format.isLenient = false
            format.parse(dateString)
            true
        } catch (e: Exception) {
            false
        }
    }
    
    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
